# NHANES Obesity and Biomarkers Study (2017–2020)

---

## Why This Project Exists

As a physician assistant with experience in both surgical and clinical research settings, I've ordered hundreds of metabolic panels, lipid profiles, and hormone labs. I know what these numbers look like at the bedside — but I wanted to understand what they look like at the population level.

This project started with a clinical question I kept coming back to: **which biomarkers actually track meaningfully with obesity, and which ones are just noise?**

That question matters. In real-world clinical practice, providers use BMI as a blunt instrument. But BMI alone doesn't tell you what's happening metabolically. Understanding which lab markers move with obesity — and how strongly — has direct implications for screening protocols, clinical trial eligibility criteria, and population health monitoring.

This project is my attempt to bring a clinician's intuition to a data analyst's toolkit.

---

## What I Found (The Short Version)

- **SHBG is the strongest signal:** Sex Hormone Binding Globulin showed a statistically significant inverse association with BMI in males aged 20–49 (OR = 0.50, 95% CI: 0.45–0.56). This is clinically meaningful — SHBG suppression in obesity is a known but underutilized marker of metabolic dysfunction.
- **Urine biomarkers disappointed:** Albumin, creatinine, and iodine showed no meaningful correlation with obesity outcomes in this dataset — a finding worth noting for researchers designing renal endpoints in obesity trials.
- **Glucose markers trended as expected** but weren't strong enough to anchor a predictive model on their own, which pushed this project from predictive to exploratory in design.

The honest pivot from predictive to exploratory modeling mid-project reflects real-world data analysis — the data tells you what it can support.

---

## Data Source

- NHANES 2017–2020 pre-pandemic cycles (CDC)
- Public population health survey with linked lab, demographic, and anthropometric data
- [Raw data available here](https://wwwn.cdc.gov/nchs/nhanes/)

---

## Technical Approach

### Data Architecture
Raw NHANES XPT files were processed through Python-based ETL pipelines and loaded into a **PostgreSQL relational database**, with each domain (demographics, urine biomarkers, blood biomarkers) stored as a separate table linked via `participant_id`. This structure enables modular querying and reproducible analysis — the same design pattern used in clinical research data management systems.

### Data Processing Pipeline
→ [ETL notebooks](./notebooks/01_data_cleaning)

Key steps:
- Column standardization and participant ID mapping across datasets
- Missing value handling with documented logic (`get_common_nan_ids()`, `drop_rows_with_common_nan_ids()`)
- Feature selection based on clinical relevance, not just statistical availability
- Export to structured PostgreSQL tables

### Analysis Modules

**1. [Urine Biomarkers](https://github.com/eudorach/portfolio_ds_projects/blob/main/NHANES_analysis/notebooks/02_analysis/3.urine_lab_analysis_intergroup.ipynb)**
Albumin, creatinine, iodine — log-transformed for skewed distributions, analyzed via correlation and linear regression, stratified by sex.

**2. Blood Biomarkers**
- [Glucose metabolism](./notebooks/02_analysis/4.blood_lab_carbohydrate_metabolism.ipynb): fasting glucose, HbA1c, insulin
- Lipid panel (in progress): total cholesterol, HDL, LDL, triglycerides

**3. [Sex Hormones — SHBG](./notebooks/02_analysis/7_blood_lab_SHBG.ipynb)**
Analysis restricted to males aged 20–49 to control for hormonal variability across menstrual cycles in females. SHBG's inverse relationship with BMI was the project's most clinically meaningful finding.

### Statistical Methods
- Pearson / Spearman correlation
- Ordinary Least Squares regression
- Stratified subgroup analysis
- Tools: pandas, numpy, scipy, statsmodels, seaborn, matplotlib

---

## Real-World Evidence Implications

This type of analysis — mining population-level observational data to surface biomarker-outcome associations — is foundational to real-world evidence generation. The NHANES dataset is structurally similar to the kinds of large, heterogeneous datasets used in RWE research: messy, incomplete, and requiring careful domain knowledge to interpret correctly.

Knowing *which* labs to trust, *why* certain subgroups need stratification, and *when* a finding is clinically meaningful versus statistically incidental — that judgment comes from clinical experience. That's what I bring to this work.

---

## Reproducibility

All analysis notebooks query directly from the PostgreSQL database rather than flat files, ensuring a consistent, reproducible data layer across the project.

---

*This project is ongoing. Future directions include multivariate modeling and expansion to NHANES dietary and physical activity data.*
