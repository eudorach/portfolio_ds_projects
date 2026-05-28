import pandas as pd
import numpy as np
import seaborn as sns
import os
import pyreadstat  # since the data files are .xpt files, this library is needed to import the table
import re
from bs4 import BeautifulSoup
import requests


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def to_snake_case(text):
    """Converts a string to snake_case."""
    text = text.lower()
    text = text.replace("-", "_")            # Hyphens → underscores
    text = text.replace("/", "_")            # Slashes → underscores
    text = re.sub(r"[^\w\s_]", "", text)     # Remove punctuation except underscores
    text = re.sub(r"\s+", "_", text)         # Spaces → underscores
    text = text.replace(",", "_")
    return text


def load_xpt(path: str) -> pd.DataFrame:
    """Loads a .xpt (SAS transport) file and returns a DataFrame."""
    df, meta = pyreadstat.read_xport(path)
    return df


def save_to_postgres(df, table_name, engine):
    """Saves a DataFrame to PostgreSQL, replacing the table if it exists."""
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
    print(f"{table_name} saved to PostgreSQL")


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTRY & CODEBOOK
# ═══════════════════════════════════════════════════════════════════════════════

def scrape_codebook(table_name, year_start=2017):
    """
    Fetches the CDC codebook page for a given table and extracts:
    - variable name (raw NHANES code, e.g. LBXGH)
    - label (human-readable description)
    - unit (if available)

    Parameters
    ----------
    table_name : str  — NHANES table name (e.g. 'LAB_GHB')
    year_start : int  — First year of the NHANES cycle (e.g. 2017, 2019, 2021).
                        Defaults to 2017 for the 2017-2020 pre-pandemic cycle.

    Returns
    -------
    List of dicts, one per variable.
    """
    url = f"https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/{year_start}/DataFiles/{table_name}.htm"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ✗ Failed to fetch {table_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    for block in soup.find_all("div", class_="pagebreak"):
        h3 = block.find("h3")
        if not h3:
            continue
        h3_text = h3.get_text(separator=" ", strip=True)
        parts   = h3_text.split(" - ", 1)
        raw_col = parts[0].strip().upper()
        label   = parts[1].strip() if len(parts) > 1 else ""

        unit = ""
        unit_match = re.search(r'\(([^)]+)\)\s*$', label)
        if unit_match:
            unit  = unit_match.group(1).strip()
            label = label[:unit_match.start()].strip()

        skip_patterns = [
            r'^WTSA',
            r'^WTSAF',
            r'^SDMVPSU',
            r'^SDMVSTRA',
            r'_LC$',
            r'SI$',
        ]
        if any(re.search(pat, raw_col) for pat in skip_patterns):
            continue
        if raw_col == "SEQN":
            continue

        records.append({
            "source_table": table_name,
            "raw_col":      raw_col,
            "label":        label,
            "unit":         unit,
            "year_start":   year_start,
        })

    return records


# ═══════════════════════════════════════════════════════════════════════════════
# TABLE BUILDERS
# ═══════════════════════════════════════════════════════════════════════════════

def build_participant_long_table(engine, registry_table, id_col, cycle=None, value_col="value"):
    """
    Generic long-table builder for any NHANES registry.

    Parameters
    ----------
    engine         : SQLAlchemy engine
    registry_table : str — registry table name (e.g. "biomarker_registry", "medhx_registry")
    id_col         : str — the ID column in the registry (e.g. "biomarker_id", "medhx_id")
    cycle          : str, optional — survey cycle label (e.g. "2017-2020"). Defaults to None.
    value_col      : str — name for the output value column (default "value")

    Returns
    -------
    Long-format DataFrame with one row per participant per registry item.
    """

    # 1. Load the registry
    registry = pd.read_sql(f"SELECT {id_col}, raw_col, source_table FROM {registry_table}", engine)

    # 2. Group registry by source table
    tables = registry.groupby("source_table")

    all_chunks = []

    for table_name, group in tables:
        print(f"Processing {table_name}...", end=" ")

        # 3. Load raw table
        raw_df = pd.read_sql(f"SELECT * FROM {table_name}", engine)

        # Standardize participant ID
        if "SEQN" in raw_df.columns:
            raw_df = raw_df.rename(columns={"SEQN": "participant_id"})

        # 4. Find which registry columns actually exist in this table
        valid = group[group["raw_col"].isin(raw_df.columns)]

        if valid.empty:
            print(f"⚠ No matching columns found, skipping")
            continue

        # 5. Keep only participant_id + relevant columns
        cols_to_keep = ["participant_id"] + valid["raw_col"].tolist()
        raw_df = raw_df[cols_to_keep]

        # 6. Add cycle column before melting
        raw_df["cycle"] = cycle

        # 7. Melt wide → long
        melted = raw_df.melt(
            id_vars=["participant_id", "cycle"],
            value_vars=valid["raw_col"].tolist(),
            var_name="raw_col",
            value_name=value_col
        )

        # 8. Swap raw_col → registry ID
        melted = melted.merge(valid[["raw_col", id_col]], on="raw_col")
        melted = melted[["participant_id", id_col, value_col, "cycle"]]

        # 9. Drop null values
        melted = melted.dropna(subset=[value_col])

        all_chunks.append(melted)
        print(f"✓ {len(melted)} rows")

    # 10. Combine all chunks
    result = pd.concat(all_chunks, ignore_index=True)
    print(f"\nTotal rows: {len(result):,}")

    return result


def build_participant_demographics(engine, cycle=None):
    """
    Builds the participant_demographics table by merging demographics,
    body measures, and blood pressure data.

    Parameters
    ----------
    engine : SQLAlchemy engine
    cycle  : str, optional — survey cycle label (e.g. "2017-2020"). Defaults to None.

    Returns
    -------
    DataFrame with one row per participant and standardized column names.
    """

    # 1. Load the 3 raw tables
    bp = pd.read_sql(
        'SELECT "SEQN", "BPXOSY1", "BPXODI1" FROM raw_bposcillometric_p_bpxo', engine
    )
    bmx = pd.read_sql(
        'SELECT "SEQN", "BMXBMI", "BMXWAIST", "BMXHT", "BMXWT" FROM raw_bmx', engine
    )
    demo = pd.read_sql("""
        SELECT "SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH3",
               "WTMECPRP", "SDMVPSU", "SDMVSTRA", "INDFMPIR"
        FROM raw_demographics
    """, engine)

    # 2. Standardize participant ID
    for df in [bp, bmx, demo]:
        df.rename(columns={"SEQN": "participant_id"}, inplace=True)

    # 3. Rename to human-readable names
    bp = bp.rename(columns={
        "BPXOSY1": "systolic_bp",
        "BPXODI1": "diastolic_bp"
    })

    bmx = bmx.rename(columns={
        "BMXBMI":   "bmi",
        "BMXWAIST": "waist_cm",
        "BMXHT":    "height_cm",
        "BMXWT":    "weight_kg"
    })

    demo = demo.rename(columns={
        "RIAGENDR": "sex",
        "RIDAGEYR": "age",
        "RIDRETH3": "race_ethnicity",
        "WTMECPRP": "survey_weight",
        "SDMVPSU":  "psu",
        "SDMVSTRA": "strata",
        "INDFMPIR": "poverty_income_ratio"
    })

    # 4. Recode sex and race to human-readable labels
    demo["sex_label"] = demo["sex"].map({1: "Male", 2: "Female"})
    demo["race_ethnicity_label"] = demo["race_ethnicity"].map({
        1: "Mexican American",
        2: "Other Hispanic",
        3: "Non-Hispanic White",
        4: "Non-Hispanic Black",
        6: "Non-Hispanic Asian",
        7: "Other/Multiracial"
    })

    # 5. Merge all three on participant_id
    df = demo.merge(bmx, on="participant_id", how="left")
    df = df.merge(bp,  on="participant_id", how="left")

    # 6. Add cycle
    df["cycle"] = cycle

    print(f"Shape: {df.shape}")
    print(f"Participants: {df['participant_id'].nunique():,}")

    return df