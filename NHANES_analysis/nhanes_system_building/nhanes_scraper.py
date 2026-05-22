"""
NHANES 2017-2020 Pre-Pandemic Biomarker Registry Scraper
---------------------------------------------------------
Scrapes all lab codebook pages from the CDC website and builds
a biomarker_registry table ready to insert into PostgreSQL.

Output: biomarker_registry.csv

Usage:
    pip install requests beautifulsoup4 pandas
    python nhanes_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# ── 1. All pre-pandemic lab table names (P_ prefix, no suffix letters) ─────────
# Extracted from: https://wwwn.cdc.gov/nchs/nhanes/search/datapage.aspx?Component=Laboratory&Cycle=2017-2020

LAB_TABLES = [
    "P_ALB_CR",    # Albumin & Creatinine - Urine
    "P_SSAGP",     # Alpha-1-Acid Glycoprotein - Serum (Surplus)
    "P_UTAS",      # Arsenic - Total - Urine
    "P_UAS",       # Arsenics - Speciated - Urine
    "P_HDL",       # Cholesterol - HDL
    "P_TRIGLY",    # Cholesterol - LDL & Triglycerides
    "P_TCHOL",     # Cholesterol - Total
    "P_UCM",       # Chromium - Urine
    "P_CRCO",      # Chromium & Cobalt
    "P_CBC",       # Complete Blood Count with 5-Part Differential
    "P_COT",       # Cotinine and Hydroxycotinine - Serum
    "P_CMV",       # Cytomegalovirus IgG & IgM Antibodies - Serum
    "P_ETHOX",     # Ethylene Oxide
    "P_FASTQX",    # Fasting Questionnaire
    "P_FERTIN",    # Ferritin
    "P_FR",        # Flame Retardants - Urine
    "P_SSFR",      # Flame Retardants - Urine (Surplus)
    "P_FOLATE",    # Folate - RBC
    "P_FOLFMS",    # Folate Forms - Total & Individual - Serum
    "P_GHB",       # Glycohemoglobin (HbA1c)
    "P_HEPA",      # Hepatitis A
    "P_HEPB_S",    # Hepatitis B Surface Antibody
    "P_HEPBD",     # Hepatitis B Core + Surface Antigen + Hepatitis D
    "P_HEPC",      # Hepatitis C RNA, Antibody, Genotype
    "P_HEPE",      # Hepatitis E IgG & IgM
    "P_HSCRP",     # High-Sensitivity C-Reactive Protein
    "P_IHGEM",     # Mercury: Inorganic, Ethyl, Methyl - Blood
    "P_INS",       # Insulin
    "P_UIO",       # Iodine - Urine
    "P_FETIB",     # Iron Status - Serum
    "P_PBCD",      # Lead, Cadmium, Total Mercury, Selenium, Manganese - Blood
    "P_UHG",       # Mercury: Inorganic - Urine
    "P_UM",        # Metals - Urine
    "P_UNI",       # Nickel - Urine
    "P_OPD",       # Organophosphate Insecticides - Urine
    "P_PERNT",     # Perchlorate, Nitrate & Thiocyanate - Urine
    "P_PFAS",      # Perfluoroalkyl and Polyfluoroalkyl Substances
    "P_GLU",       # Plasma Fasting Glucose
    "P_TST",       # Sex Steroid Hormone Panel - Serum
    "P_BIOPRO",    # Standard Biochemistry Profile
    "P_TFR",       # Transferrin Receptor
    "P_UCFLOW",    # Urine Flow Rate
    "P_UCPREG",    # Urine Pregnancy Test
    "P_UVOC",      # Volatile Organic Compound Metabolites - Urine
    "P_UVOC2",     # Volatile Organic Compound Metabolites II - Urine
    "P_VOCWB",     # Volatile Organic Compounds - Blood
]

BASE_URL = "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/{table}.htm"

# ── 2. Scrape one codebook page ─────────────────────────────────────────────────

def scrape_codebook(table_name):
    """
    Fetches the CDC codebook page for a given table and extracts:
    - variable name (raw NHANES code, e.g. LBXGH)
    - label (human-readable description)
    - unit (if available)
    Returns a list of dicts, one per variable.
    """
    url = BASE_URL.format(table=table_name)
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ✗ Failed to fetch {table_name}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    # Each variable in the codebook has a <div class="pagebreak"> block
    # with an <h3> tag (variable name) and a <dl> tag (details)
    for block in soup.find_all("div", class_="pagebreak"):
        h3 = block.find("h3")
        if not h3:
            continue

        # Variable name is in the <h3> tag, e.g. "LBXGH - Glycohemoglobin (%)"
        h3_text = h3.get_text(separator=" ", strip=True)

        # Split on " - " to get variable name vs label
        parts = h3_text.split(" - ", 1)
        raw_col = parts[0].strip().upper()
        label   = parts[1].strip() if len(parts) > 1 else ""

        # Extract unit from label if in parentheses at the end, e.g. "HbA1c (%)"
        unit = ""
        unit_match = re.search(r'\(([^)]+)\)\s*$', label)
        if unit_match:
            unit = unit_match.group(1).strip()
            label = label[:unit_match.start()].strip()

        # Skip non-measurement variables (weights, comment codes, etc.)
        skip_patterns = [
            r'^WTSA',   # sample weights
            r'^WTSAF',
            r'^SDMVPSU',
            r'^SDMVSTRA',
            r'_LC$',    # below lower limit of detection flags
            r'SI$',     # SI unit duplicates
        ]
        if any(re.search(pat, raw_col) for pat in skip_patterns):
            continue

        # Skip SEQN (participant ID — handled separately)
        if raw_col == "SEQN":
            continue

        records.append({
            "source_table": table_name,
            "raw_col":      raw_col,
            "label":        label,
            "unit":         unit,
        })

    return records


# ── 3. Scrape all tables ────────────────────────────────────────────────────────

def build_registry(tables):
    all_records = []
    total = len(tables)

    for i, table in enumerate(tables, 1):
        print(f"[{i}/{total}] Scraping {table}...")
        records = scrape_codebook(table)
        all_records.extend(records)
        print(f"       → {len(records)} variables found")
        time.sleep(0.5)   # be polite to CDC servers

    return all_records


# ── 4. Clean and export ─────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("NHANES 2017-2020 Pre-Pandemic Biomarker Registry Scraper")
    print("=" * 55)

    records = build_registry(LAB_TABLES)

    if not records:
        print("\n✗ No records scraped. Check your internet connection.")
        return

    df = pd.DataFrame(records)

    # Add auto-increment biomarker_id
    df.insert(0, "biomarker_id", range(1, len(df) + 1))

    # Add a clean snake_case biomarker_name column from the label
    def to_snake(text):
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", "_", text.strip())
        return text[:60]   # cap length

    df["biomarker_name"] = df["label"].apply(to_snake)

    # Reorder columns to match the registry schema
    df = df[["biomarker_id", "biomarker_name", "raw_col", "label", "unit", "source_table"]]

    # Save to CSV
    out_path = "biomarker_registry.csv"
    df.to_csv(out_path, index=False)

    print(f"\n✓ Done! {len(df)} variables scraped from {len(LAB_TABLES)} tables.")
    print(f"✓ Saved to: {out_path}")
    print("\nPreview:")
    print(df.head(10).to_string(index=False))

    # ── 5. Print the SQL to create + load the table in PostgreSQL ───────────────
    print("\n" + "=" * 55)
    print("SQL to create the registry table in PostgreSQL:")
    print("=" * 55)
    print("""
CREATE TABLE IF NOT EXISTS staging.biomarker_registry (
    biomarker_id    SERIAL PRIMARY KEY,
    biomarker_name  TEXT NOT NULL,   -- snake_case human-readable name
    raw_col         TEXT NOT NULL,   -- original NHANES column code
    label           TEXT,            -- full description
    unit            TEXT,            -- measurement unit (%, mg/dL, etc.)
    source_table    TEXT             -- NHANES table name (e.g. P_GHB)
);

-- Then load the CSV:
COPY staging.biomarker_registry (biomarker_name, raw_col, label, unit, source_table)
FROM '/path/to/biomarker_registry.csv'
CSV HEADER;
""")


if __name__ == "__main__":
    main()
