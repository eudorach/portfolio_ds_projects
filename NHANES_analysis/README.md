# NHANES Obesity and Biomarkers Study (2017–2020)

---

## Overview
This project investigates associations between obesity (BMI) and clinical biomarkers using NHANES 2017–2020 data. The focus is on metabolic, renal, and endocrine markers and their relationship to obesity-related outcomes.

Data was processed into a relational PostgreSQL database to enable reproducible analysis and modular querying.

---

## Objective
To evaluate how physiological biomarkers relate to obesity across multiple systems:

- Kidney function (urine biomarkers)
- Glucose metabolism
- Lipid metabolism
- Thyroid-related metabolism
- Sex hormone regulation

---

## Data Source
- NHANES 2017–2020 cycles (CDC)
- Public health survey dataset
- Data structured into a PostgreSQL relational database

---

## [Data Pipeline Overview](./notebooks/01_data_cleaning)
Raw NHANES datasets were processed using Python-based ETL pipelines.

Key steps included:
- Column standardization
- Handling missing values
- Feature selection based on clinical relevance
- Export to relational database tables

Each dataset was stored as a separate table linked via `participant_id`.

---

## Dataset Structure

Final database includes:

- Demographics
- Anthropometric measurements
- Urine biomarkers
- Blood biomarkers
- Specialized biomarker subsets

---

## Analysis Design

### 1. [Urine Biomarkers](./notebooks/02_analysis/3.urine_lab_analysis_intergroup.ipynb)
Analyzed biomarkers:
- Albumin
- Creatinine
- Iodine

Methods:
- Log transformation for skewed distributions
- Correlation analysis
- Linear regression
- Sex-stratified analysis

---

### 2. Blood Biomarkers
Includes:
- CBC with differential
- Glucose metabolism markers
  - Fasting glucose
  - HbA1c
  - Insulin
- Lipid panel

---

### 3. Sex Hormones
Focus:
- [Sex Hormone Binding Globulin (SHBG)](./notebooks/02_analysis/7_blood_lab_SHBG.ipynb)
- Male cohort (20–49 years)

Rationale:
Controlled subgroup chosen due to hormonal variability in females across menstrual cycles.

---

## Methodology Summary
- Python (pandas, numpy) for preprocessing
- PostgreSQL for structured storage
- Statistical analysis in Python (scipy, statsmodels)
- Visualization using seaborn and matplotlib

Methods used:
- Pearson / Spearman correlation
- Ordinary Least Squares regression
- Stratified subgroup analysis

---

## Reproducibility
All processed datasets are stored in a PostgreSQL relational database. Analysis notebooks query directly from this database to ensure reproducibility and modular workflow design.

---

## Data Cleaning (Detailed Documentation)

Detailed preprocessing steps, functions, and transformations are documented in the ETL notebooks.

Key utilities include:
- `standardize_id_column()` → ensures consistent participant ID mapping
- `get_common_nan_ids()` → identifies overlapping missing values
- `drop_rows_with_common_nan_ids()` → filters incomplete paired observations

Column renaming and feature engineering are documented within each dataset-specific cleaning notebook.

---

## Data Source
https://wwwn.cdc.gov/nchs/nhanes/
