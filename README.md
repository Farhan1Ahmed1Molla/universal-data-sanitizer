# 🧹 Universal Data Sanitizer & Auditor

An automated, production-grade Python CLI pipeline designed to ingest raw, corrupted, or messy CSV files and output an analysis-ready dataset. Built to handle the unpredictable edge cases found in real-world client spreadsheets.

## 🚀 The Problem
Clients often export data from legacy systems with missing values, inconsistent date formats, disguised nulls (e.g., "N/A", "unknown", "-"), and mixed text/numeric data types. Manual cleaning is slow, error-prone, and threatens data integrity.

## 🛠️ The Solution
This CLI tool applies a multi-layer defense to standardize data in seconds:
1. **Auto-Delimiter Detection:** Uses `csv.Sniffer` to automatically detect whether a file uses commas, semicolons, tabs, or pipes.
2. **Header Normalization:** Strips whitespace, lowercases, and replaces spaces with underscores.
3. **Duplicate Removal:** Drops 100% identical rows to prevent data bloat.
4. **Disguised Null Detection:** Scans text columns for fake nulls (`n/a`, `null`, `?`, `tbd`) and converts them to true `NaN` values.
5. **Smart Numeric Scrubbing:** Strips currency symbols (`$`, `₹`, `€`), commas, and unit suffixes (`GB`, `kg`, `lbs`) before safely converting them to floats using `errors='coerce'` to handle corrupt entries.
6. **Auto-Date Parsing:** Detects date columns and standardizes them to `datetime` objects.

## 🧪 Testing & Reliability
This project includes a comprehensive `pytest` suite to guarantee data integrity. It covers header normalization, duplicate removal, date parsing, and delimiter sniffing.

To run the tests locally:
```bash
pip install -r requirements.txt
pytest
