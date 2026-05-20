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