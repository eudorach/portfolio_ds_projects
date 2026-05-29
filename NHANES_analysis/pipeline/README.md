# NHANES Biomarker Analysis Pipeline

A reusable epidemiological analysis pipeline for exploring biomarker-disease relationships using the **NHANES 2017–2020 Pre-Pandemic dataset** — built by a clinician transitioning into data analytics.

*Evolved from exploratory analysis of the datasets (see [exploratory](../exploratory) folder)*

---

## The Problem with Most NHANES Analyses

Most NHANES analyses are written once, for one question, hardcoding column names like `LBXGH` and `BMXBMI` throughout. When the question changes, the code has to be rewritten.

This pipeline was built to solve that. One consistent architecture. Any biomarker. Any disease. Any medical history variable. No rewriting.

---

## What I Built

**39 laboratory tables** (347 biomarkers) and **11 medical history/questionnaire tables** (279 variables) loaded into PostgreSQL, structured around a long table design with a registry at its core for each data type.

```
Raw XPT Files
      ↓
PostgreSQL (raw schema)                    ← automated batch ingestion via ingest_folder()
      ↓
biomarker_registry  (347 biomarkers)       ← auto-scraped from CDC codebooks
medhx_registry      (279 variables)        ← diet, medications, smoking, reproductive health, and more
      ↓
participant_biomarkers   (2,093,413 rows)  ← long format: one row per participant per biomarker
participant_medhx        (1,536,554 rows)  ← long format: one row per participant per med history item
participant_demographics (15,560 rows)     ← outcomes + covariates
      ↓
nhanes_analysis.py                         ← reusable analysis functions
```

The registry pattern is the key architectural decision. Adding a new biomarker or medical history variable means inserting one row into the relevant registry — no schema changes, no rewriting analysis code. NHANES column codes (`LBXGH`, `URXUMA`, etc.) never appear outside the registry.

Codebooks for all 39 lab tables and 11 medical history tables were automatically scraped from the CDC website at build time, extracting variable names, human-readable labels, and units — eliminating manual data dictionary lookup entirely.

---

## Analyses

Three analyses were conducted to validate the pipeline across different biomarker panels and disease contexts.

### [1. Urine Biomarkers vs Obesity](./notebooks/analysis/1.urine_bmi_analysis.ipynb)
**Cohort:** Adults ≥ 18 (n = 2,898) | **Biomarkers:** Albumin, creatinine, iodine

Low predictive power (R² = 0.053). Only creatinine reached significance — likely reflecting its association with muscle mass rather than adiposity. These markers measure renal function, not fat.

### [2. Carbohydrate Metabolism vs Obesity](./notebooks/analysis/2.blood_carbohydrate_metabolism.ipynb)
**Cohort:** Adults ≥ 18, diabetics excluded (n = 3,478) | **Biomarkers:** Insulin, HbA1c, fasting glucose

Strong associations (R² = 0.329). Insulin was the strongest correlate of BMI (r = 0.556). Each 1% increase in HbA1c was associated with 2.26× higher odds of obesity. Fasting glucose excluded from regression due to multicollinearity with HbA1c.

### [3. SHBG vs Obesity in Males 22–49](./notebooks/analysis/3.shbg_bmi_analysis.ipynb)
**Cohort:** Males aged 22–49 (n = 1,387) | **Biomarker:** SHBG

(./figures/shbg_distribution.png)
(./figures/shbg_quartile_forest.png)

Strong inverse relationship (r = −0.352). Each 1 nmol/L increase in SHBG = 5.3% lower odds of obesity (OR = 0.947), consistent with known links between low SHBG, insulin resistance, and metabolic syndrome.

In progress: female cohort SHBG analysis
---

## Analysis Functions

All functions share the same interface — pass biomarkers, a disease, and optional filters:

```python
filters = {"age_range": (22, 49), "sex": 1, "exclude_diabetes": True}

run_cohort_descriptives(biomarkers, disease, engine, filters)
run_biomarker_descriptives(biomarkers, disease, engine, filters)
run_distribution_plots(biomarkers, disease, engine, filters)
run_correlation(biomarkers, disease, engine, method, log_transform, filters)
run_linear_regression(biomarkers, disease, engine, log_transform, filters, covariates)
run_logistic_regression(biomarkers, disease, engine, log_transform, filters, covariates)
run_quartile_analysis(biomarker, disease, engine, log_transform, filters, covariates)
```

Covariates default to age, sex, and race/ethnicity but are fully configurable — medical history variables from `participant_medhx` can be passed in directly. Disease outcomes are defined once in `diagnosis_config.py` (WHO, ACC/AHA, ADA criteria) and reused across all analyses.

---

## Methodological Notes

- **Log transformation** applied for correlation and linear regression to address right skewness. Not applied for logistic regression — preserves clinically interpretable odds ratios
- **Covariate adjustment** for age, sex, and race/ethnicity across all models. Sex auto-excluded when a single-sex filter is applied
- **Survey weights** collected and stored (`WTMECPRP`, PSU, strata) for future complex survey analysis
- **Missing data** handled via complete case analysis
- **Hormonal contraceptive exclusion** not applied due to incomplete medication capture in NHANES; noted as a limitation in hormone-related analyses

---

## Stack

Python · PostgreSQL · pandas · statsmodels · SQLAlchemy · seaborn · BeautifulSoup · scikit-learn

---

## Data Source

CDC NHANES 2017–March 2020 Pre-Pandemic: https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020

---
*For database schema, setup instructions, and function reference → [TECHNICAL.md](TECHNICAL.md)*
