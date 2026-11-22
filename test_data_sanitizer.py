"""
test_data_sanitizer.py

One test per cleaning rule. Run with: pytest
"""

import pandas as pd
from data_sanitizer import detect_delimiter, sanitize_data


def test_strips_whitespace():
    df = pd.DataFrame({"name": ["  Bob  "]})
    result = sanitize_data(df)
    assert result["name"][0] == "Bob"


def test_normalizes_headers():
    df = pd.DataFrame({" First Name! ": ["Bob"]})
    result = sanitize_data(df)
    assert "first_name" in result.columns


def test_removes_duplicates():
    df = pd.DataFrame({"name": ["Bob", "Bob"]})
    result = sanitize_data(df)
    assert len(result) == 1


def test_standardizes_dates():
    df = pd.DataFrame({"sale_date": ["2024-01-15", "01/16/2024"]})
    result = sanitize_data(df)
    assert pd.api.types.is_datetime64_any_dtype(result["sale_date"])


def test_handles_odd_delimiters(tmp_path):
    messy_file = tmp_path / "semicolon.csv"
    messy_file.write_text("name;age\nBob;30\n")
    delimiter = detect_delimiter(messy_file)
    assert delimiter == ";"
