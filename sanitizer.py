import pandas as pd
import numpy as np
import re

def sanitize_data(df):
    clean_df = df.copy()

    # LAYER 1: Standardize Column Headers
    clean_df.columns = (
        clean_df.columns
        .str.strip()
        .str.lower()
        .str.replace(r'[^\w\s]', '', regex=True)
        .str.replace(r'\s+', '_', regex=True)
    )

    # LAYER 2: Drop 100% Duplicate Rows
    initial_rows = len(clean_df)
    clean_df = clean_df.drop_duplicates().reset_index(drop=True)
    dupes_removed = initial_rows - len(clean_df)

    # LAYER 3: Clean Text Columns & Convert Disguised Nulls
    fake_nulls = ['n/a', 'na', 'null', 'none', 'error', 'unknown', '-', '--', '?', 'tbd', '']

    for col in clean_df.select_dtypes(include='object').columns:
        clean_df[col] = clean_df[col].astype(str).str.strip()
        clean_df[col] = clean_df[col].apply(
            lambda x: np.nan if x.lower() in fake_nulls or x == 'nan' else x
        )

    # LAYERS 4 & 5: Auto-Date Parsing & Smart Numeric Scrubbing
    for col in clean_df.select_dtypes(include='object').columns:
        non_null_count = clean_df[col].notna().sum()
        if non_null_count == 0:
            continue

        # Layer 4: Dates
        if 'date' in col:
            clean_df[col] = pd.to_datetime(clean_df[col], errors='coerce', format='mixed')
            clean_df = clean_df.sort_values(by=col, ascending=True).reset_index(drop=True)
            continue

        # Layer 5: Numbers
        temp_num = clean_df[col].str.replace(r'[$€£₹,%]', '', regex=True).str.strip()
        converted_num = pd.to_numeric(temp_num, errors='coerce')

        if (converted_num.notna().sum() / non_null_count) >= 0.70:
            clean_df[col] = converted_num

    # FINAL OUTPUT (Must stay at the very bottom of the function)
    print(f"Headers standardized | Duplicate rows removed: {dupes_removed}")
    return clean_df
