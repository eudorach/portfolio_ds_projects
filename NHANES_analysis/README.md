> **Update:** This project has evolved into a fully reusable analysis pipeline.
> See the [NHANES Biomarker Analysis Pipeline](./pipeline/README.md) for the latest version.

# NHANES Obesity and Biomarkers Study (2017–2020)

---

## Why This Project Exists

As a physician assistant with experience in both surgical and clinical research settings, I've ordered hundreds of metabolic panels and lipid profiles. I know what these numbers look like at the bedside — but I wanted to understand what they look like at the population level.

This project started with a clinical question I kept coming back to: **which biomarkers actually track meaningfully with obesity, and which ones are just noise?**

That question matters. In real-world clinical practice, providers use BMI as a blunt instrument. But BMI alone doesn't tell you what's happening metabolically. Understanding which lab markers move with obesity — and how strongly — has direct implications for screening protocols, clinical trial eligibility criteria, and population health monitoring.

This project is my attempt to bring a clinician's intuition to a data analyst's toolkit.

---

## What I Found (The Short Version)

**Glucose metabolism (n = 3,146 adults):**
- **Fasting insulin is the dominant metabolic signal**, showing the strongest and most consistent association with BMI (r = 0.41 overall; males: r = 0.42, females: r = 0.43). In adjusted logistic regression, each 1 µU/mL increase in fasting insulin was independently associated with higher odds of obesity (OR = 1.14, 95% CI: 1.13–1.16, p < 0.001).
- **HbA1c shows a particularly strong adjusted association with obesity** — each 1% increase corresponded to approximately two-fold higher odds of obesity (OR = 2.11, 95% CI: 1.62–2.74, p < 0.001), reflecting the contribution of chronic glycemic burden beyond fasting insulin alone. Sex-stratified correlations showed stronger associations in females (r = 0.26) than males (r = 0.15).
- **Fasting glucose is the weakest of the three** (r = 0.23), consistent with its tighter physiological regulation and lower sensitivity to early metabolic dysfunction.
- **Combined metabolic markers explain meaningful variance in BMI** — the multivariable OLS model adjusted for age, sex, and race/ethnicity achieved R² ≈ 0.24, compared to R² ≈ 0.10–0.21 for single-predictor models. The adjusted logistic regression model demonstrated moderate explanatory performance (Pseudo R² ≈ 0.22).
- **Demographic covariates were independently associated with obesity:** female sex (OR = 1.65, 95% CI: 1.39–1.96), age (OR ≈ 0.99/year, small inverse effect), and race/ethnicity showed heterogeneous associations across groups — findings that contextualize the biomarker results within known population-level disparities.

**Sex hormones (n = 1,447 adult males aged 20–49):**
- **SHBG showed a strong, dose-dependent inverse association with obesity** — each increase in SHBG quartile corresponded to lower odds of obesity (OR = 0.50, 95% CI: 0.45–0.56, p < 0.001) after adjustment for age and race/ethnicity. Adjusted predicted probabilities confirmed a monotonic decrease in obesity risk across increasing quartiles, supporting the consistency of the association. Age was independently associated with higher odds of obesity (OR ≈ 1.02–1.05 per year). Analysis was restricted to males aged 20–49 to control for hormonal variability across the menstrual cycle in females. Due to the cross-sectional design, reverse causation — where increased adiposity drives SHBG suppression — cannot be excluded.

**Urine biomarkers:**
- Albumin, creatinine, and iodine showed no meaningful correlation with obesity outcomes — a finding worth noting for researchers designing renal endpoints in obesity trials.

**A note on modeling approach:** Early in this project, single-biomarker correlations appeared too weak to anchor a predictive model. The glucose metabolism analysis clarified why — no individual marker carries enough signal, but combined metabolic markers together explain clinically relevant variance. The analytical design evolved accordingly, which is how real-world data analysis actually works.

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
- Multivariable linear regression (adjusted for age, sex, race/ethnicity)
- Binary logistic regression (obesity as outcome, BMI ≥ 30 kg/m²)
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
