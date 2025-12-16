# Data Cleaning & Analysis Pipeline – UK-500 Dataset

This project demonstrates my work as a **Data Analyst** on the *UK-500* dataset, containing contact information for UK companies and individuals.  
It covers the full data workflow: data cleaning, feature engineering, analysis, grouping, and exporting results.

---

## Key Steps & Skills

### 1. Data Import & Exploration
- Loaded CSV dataset (`uk-500.csv`)
- Checked data types, missing values, duplicates, and basic statistics
- Assessed initial data quality

### 2. Data Cleaning
- Standardized text columns (names, cities, companies)
- Normalized emails and websites (lowercase, removed extra spaces)
- Standardized phone numbers with custom function `clean_phone()`
- Unified text formatting with `standartize_text()`
- Handled missing values and duplicates

### 3. Feature Engineering
- `full_name` — combined first and last name
- `email_domain` — extracted domain from email
- `city_length` — length of city name
- `is_gmail` — Gmail user flag

### 4. Filtering & Sampling
- Gmail users subset
- Companies containing `LLC` or `Ltd`
- Users in London
- Companies with long names (4+ words)
- Positional sampling and random sampling for analysis

### 5. Grouping & Analysis
- City frequency counts (`value_counts()`)
- Aggregation by city: total users & unique email domains
- Analysis of top email domains
- Identified patterns and user concentration

### 6. Export
- `uk500_clean.csv` — cleaned dataset
- `gmail_users.csv` — Gmail users subset
- `stats.xlsx` — Top Cities & Top Domains sheets

---
## Most Valuable Transformations

Key transformations that significantly improved data quality:

- phone number normalization for deduplication;
- email standardization and domain extraction;
- unified text formatting across all string columns;
- creation of analytical features for deeper insights.

---

## Key Findings
- London and other major cities have the highest number of users
- Gmail is the most common email provider among users
- Data had inconsistent phone/email formats and duplicates

---


## Possible Future Improvements

Potential enhancements for future iterations of the project:

- deduplication by email or phone number;
- email validation using regular expressions;
- website normalization (protocol handling, removing `www`);
- geographic analysis using maps;
- data visualization (matplotlib / seaborn);
- refactoring into reusable modules.

---

## Project Summary

This project demonstrates my ability to:

- clean and standardize real-world datasets;
- design custom data cleaning functions;
- perform feature engineering and exploratory analysis;
- generate actionable insights through grouping and filtering;
- prepare clean, structured data for further analytics or machine learning tasks.
