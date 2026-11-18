# 🧹 Universal Data Sanitizer & Auditor

An automated Python pipeline designed to ingest raw, corrupted, or messy CSV files and output an analysis-ready dataset. Built to handle the unpredictable edge cases found in real-world client spreadsheets.

## 🚀 The Problem
Clients often export data from legacy systems with missing values, inconsistent date formats, disguised nulls (e.g., "N/A", "unknown", "-"), and mixed text/numeric data types. Manual cleaning is slow, error-prone, and threatens data integrity.

## 🛠️ The Solution
This script applies a multi-layer defense to standardize data in seconds:
1. **Header Normalization:** Strips whitespace, lowercases, and replaces spaces with underscores.
2. **Duplicate Removal:** Drops 100% identical rows to prevent data bloat.
3. **Disguised Null Detection:** Scans text columns for fake nulls (`n/a`, `null`, `?`, `tbd`) and converts them to true `NaN` values.
4. **Smart Numeric Scrubbing:** Automatically detects columns that should be numbers (removing currency symbols like `$`, `₹`, `€` and commas) and safely converts them, using `errors='coerce'` to handle corrupt entries.
5. **Auto-Date Parsing:** Detects date columns and standardizes them to `datetime` objects, immediately sorting the dataframe chronologically.

## 📂 Case Studies & Proof of Work

To prove the pipeline works on real-world chaos, I have run it against 3 Kaggle datasets and documented the domain-specific logic required to fix them:

### 1. Cafe Sales Audit (Notebook: `case_studies_01_cafe_sales_audit.ipynb`)
*   **The Chaos:** 10,000 rows, missing values across 8 columns, hidden text in numeric columns.
*   **The Fix:** After running the universal sanitizer, I wrote domain-specific recovery logic. I mapped missing `item` names by looking up their `price_per_unit`, and recalculated missing `total_spent` by verifying the `quantity * price` math.

### 2. Laptop Sales Audit (Notebook: `case_studies_02_laptop_sales_audit.ipynb`)
*   **The Chaos:** Data types were completely broken (e.g., `ram` was "8GB", `weight` was "1.37kg"). Duplicate OS names ("Mac OS X" vs "macOS").
*   **The Fix:** Used regex string manipulation (`.str.replace`) to strip text and cast to `float64`. Standardized categorical values for accurate grouping.

## 💻 Tech Stack
*   **Language:** Python 3
*   **Libraries:** Pandas, NumPy, Regex (re)

---
*Looking for custom data pipelines or need a specific dataset cleaned? Let's connect.*
