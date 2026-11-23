"""
data_sanitizer.py

Cleans a messy CSV: standardizes headers, removes duplicate rows,
converts disguised nulls (n/a, NULL, --, etc.) to real NaN, parses
date columns, strips currency/% symbols and common unit suffixes
(GB, kg, lb...) from number columns, and auto-detects the file's
delimiter (comma, semicolon, tab, pipe).

Usage:
    python data_sanitizer.py messy.csv
    -> writes messy_clean.csv in the same folder
"""

import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd

FAKE_NULLS = ["n/a", "na", "null", "none", "error", "unknown", "-", "--", "?", "tbd", ""]
NUMERIC_NOISE = r"[$€£₹,%]|(?i:\b(gb|mb|tb|kb|kg|lbs|lb)\b)"


def detect_delimiter(file_path: Path, sample_size: int = 4096) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        sample = f.read(sample_size)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        return dialect.delimiter
    except csv.Error:
        return ","


def sanitize_data(df: pd.DataFrame) -> pd.DataFrame:
    clean_df = df.copy()

    clean_df.columns = (
        clean_df.columns
        .str.strip().str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "_", regex=True)
    )

    initial_rows = len(clean_df)
    clean_df = clean_df.drop_duplicates().reset_index(drop=True)
    dupes_removed = initial_rows - len(clean_df)

    def _clean_cell(x):
        if pd.isna(x):
            return np.nan
        x = str(x).strip()
        return np.nan if x.lower() in FAKE_NULLS else x

    for col in clean_df.select_dtypes(include=["object", "string"]).columns:
        clean_df[col] = clean_df[col].apply(_clean_cell)

    for col in clean_df.select_dtypes(include=["object", "string"]).columns:
        non_null_count = clean_df[col].notna().sum()
        if non_null_count == 0:
            continue
        if "date" in col:
            clean_df[col] = pd.to_datetime(clean_df[col], errors="coerce", format="mixed")
            continue
        temp_num = clean_df[col].str.replace(NUMERIC_NOISE, "", regex=True).str.strip()
        converted_num = pd.to_numeric(temp_num, errors="coerce")
        if (converted_num.notna().sum() / non_null_count) >= 0.70:
            clean_df[col] = converted_num

    print(f"Headers standardized | Duplicate rows removed: {dupes_removed}")
    return clean_df


def main():
    parser = argparse.ArgumentParser(description="Clean a messy CSV file.")
    parser.add_argument("input_file", help="Path to the messy CSV")
    args = parser.parse_args()

    in_path = Path(args.input_file)
    delimiter = detect_delimiter(in_path)

    df = pd.read_csv(in_path, sep=delimiter)
    clean_df = sanitize_data(df)

    for col in clean_df.select_dtypes(include="string").columns:
        clean_df[col] = clean_df[col].astype(object)

    out_path = in_path.with_name(f"{in_path.stem}_clean.csv")
    try:
        clean_df.to_csv(out_path, index=False)
        print(f"Saved: {out_path}")
    except OSError:
        fallback_path = Path.cwd() / f"{in_path.stem}_clean.csv"
        clean_df.to_csv(fallback_path, index=False)
        print(f"Input folder is read-only. Saved to: {fallback_path}")


if __name__ == "__main__":
    main()

