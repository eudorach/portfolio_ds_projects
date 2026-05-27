import pandas as pd
import numpy as np
import seaborn as sns
import os
import pyreadstat #since the data files are .xpt files, this library is needed to import the table
import re
from bs4 import BeautifulSoup
import requests

def standardize_id_column(df, original_id='SEQN', new_id='participant_id'):
    """
    Renames the identifier column in a DataFrame from original_id to new_id.
    If the original_id is not present, returns the DataFrame unchanged.

    Parameters:
    - df: pandas DataFrame
    - original_id: name of the identifier column to replace (default 'SEQN')
    - new_id: standardized name to use (default 'participant_id')

    Returns:
    - DataFrame with standardized ID column
    """
    if original_id in df.columns:
        df = df.rename(columns={original_id: new_id})
    return df

def get_common_nan_ids(df, col1, col2, id_col='participant_id', verbose=True):
    """
    Returns a set of participant IDs where BOTH col1 and col2 are NaN.
    
    Parameters:
    - df: pandas DataFrame
    - col1, col2: column names to check for NaNs
    - id_col: column name for participant IDs (default 'participant_id')
    
    Returns:
    - Set of participant IDs with NaNs in both columns
    """
    ids_nan_col1 = set(df.loc[df[col1].isna(), id_col])
    ids_nan_col2 = set(df.loc[df[col2].isna(), id_col])
    common_nan_ids = ids_nan_col1.intersection(ids_nan_col2)
    
    if verbose:
        print(f"Number of NaNs in {col1}: {len(ids_nan_col1)}")
        print(f"Number of NaNs in {col2}: {len(ids_nan_col2)}")
        print(f"Number of IDs with NaNs in both columns: {len(common_nan_ids)}")
    
    return common_nan_ids

def drop_rows_with_common_nan_ids(df, col1, col2, id_col='participant_id'):
    """
    Drops rows where BOTH col1 and col2 are NaN.
    Uses get_common_nan_ids() to identify rows.
    
    Parameters:
    - df: pandas DataFrame
    - col1, col2: column names to check for NaNs
    - id_col: column name for participant IDs (default 'participant_id')
    
    Returns:
    - cleaned DataFrame (copy)
    """
    common_nan_ids = get_common_nan_ids(df, col1, col2, id_col, verbose=False)
    rows_dropped = df[id_col].isin(common_nan_ids).sum()
    
    print(f"Rows dropped where both {col1} and {col2} were NaN: {rows_dropped}")
    
    return df[~(df[col1].isna() & df[col2].isna())].copy()

# Clean text to snake_case
def to_snake_case(text):
    text = text.lower()
    text = text.replace("-", "_")            # Hyphens → underscores
    text = text.replace("/", "_")            # Slashes → underscores
    text = re.sub(r"[^\w\s_]", "", text)     # Remove punctuation except underscores
    text = re.sub(r"\s+", "_", text)         # Spaces → underscores
    text = text.replace(",","_")
    return text

def clean_nhanes_module(
    df: pd.DataFrame,
    nhanes_url: str,
    drop_cols: list[str] = None,
    id_col: str = "participant_id",
) -> pd.DataFrame:
    """
    Generic cleaner for any NHANES lab/questionnaire module.

    Parameters
    ----------
    df          : Raw DataFrame with original NHANES column names.
    nhanes_url  : URL to the NHANES HTML data dictionary for this module.
    drop_cols   : Column names (post-rename, snake_case) to drop. Defaults to [].
    id_col      : Name of the participant ID column to exclude from nan-row check.

    Returns
    -------
    Cleaned DataFrame with renamed columns, dropped columns, and
    rows removed where all non-ID values are NaN.
    """
    drop_cols = drop_cols or []

    # --- 1. Scrape rename map from NHANES data dictionary ---
    response = requests.get(nhanes_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    pattern = re.compile(r'^([A-Z0-9_]+)\s*-\s*(.+)$')
    rename_dict = {}

    for tag in soup.find_all("h3"):
        text = tag.get_text(strip=True)
        match = pattern.match(text)
        if match:
            var_name, description = match.group(1), match.group(2)
            rename_dict[var_name] = to_snake_case(description)

    # Only rename columns that actually exist in the DataFrame
    filtered = {k: v for k, v in rename_dict.items() if k in df.columns}
    df = df.rename(columns=filtered)

    # --- 2. Drop specified columns (ignore missing ones) ---
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # --- 3. Drop rows where all non-ID values are NaN ---
    value_cols = [c for c in df.columns if c != id_col]
    df = df[~df[value_cols].isna().all(axis=1)].copy()

    return df

def save_to_postgres(df, table_name, engine):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )
    print(f"{table_name} saved to PostgreSQL")

def load_xpt(path: str) -> pd.DataFrame:
    df, meta = pyreadstat.read_xport(path)
    return df

def validate(df: pd.DataFrame, name: str):
    print(f"\n---{name} ---")
    print("Shape:", df.shape)
    print("Nulls (top 5):")
    print(df.isnull().sum().sort_values(ascending=False).head(5))

# Remove the module-level BASE_URL entirely

def scrape_codebook(table_name, year_start=2017):
    """
    Fetches the CDC codebook page for a given table and extracts:
    - variable name (raw NHANES code, e.g. LBXGH)
    - label (human-readable description)
    - unit (if available)
    
    Args:
        table_name (str): NHANES table name (e.g. 'LAB_GHB')
        year_start (int): First year of the NHANES cycle (e.g. 2017, 2019, 2021)
                         Defaults to 2017 for the 2017-2020 pre-pandemic cycle.
    
    Returns a list of dicts, one per variable.
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
        parts = h3_text.split(" - ", 1)
        raw_col = parts[0].strip().upper()
        label   = parts[1].strip() if len(parts) > 1 else ""

        unit = ""
        unit_match = re.search(r'\(([^)]+)\)\s*$', label)
        if unit_match:
            unit = unit_match.group(1).strip()
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
            "year_start":   year_start,  # useful metadata to store
        })

    return records

def build_participant_long_table(engine, registry_table, id_col, cycle=None, value_col="value"):
    """
    Generic long-table builder for any NHANES registry.
    
    Parameters:
    -----------
    engine          : SQLAlchemy engine
    registry_table  : str — registry table name (e.g. "biomarker_registry", "medhx_registry")
    id_col          : str — the ID column in the registry (e.g. "biomarker_id", "medhx_id")
    cycle           : str — survey cycle label (e.g. "2017-2020", "2015-2016")
    value_col       : str — name for the output value column (default "value")
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