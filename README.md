# 🧪 Clinical & Public Health Data Analytics Portfolio

Welcome to my personal analytics portfolio. This repository contains independent projects focused on clinical, biomedical, and public health datasets.

Each project is designed to replicate real-world healthcare analytics workflows, including:
- Structured data extraction and transformation (ETL)
- SQL-based cohort and relational analysis
- Statistical modeling and regression-based inference
- Stratified and interaction-based exploratory analysis
- Careful separation of association vs. causation in observational data

The goal of this portfolio is to bridge clinical domain expertise with data science methodology, with a focus on population health and healthcare operations analytics.

---

# 📁 Projects Included

## 🧬 NHANES Obesity & Biomarkers Study (2017–2020)

A population-level analysis of metabolic, hormonal, and urinary biomarkers associated with obesity using NHANES survey data.

This project explores which physiological markers meaningfully track with BMI and obesity status, and which associations weaken under multivariable adjustment.

Key analytical components include:
- Multi-table relational database design (PostgreSQL)
- ETL pipeline development for NHANES XPT data
- Correlation and regression-based biomarker analysis
- Multivariable modeling adjusted for demographic covariates
- Stratified analysis by sex and age where clinically appropriate

Key findings highlight:
- Strong associations between insulin resistance markers (insulin, HbA1c) and obesity
- A dose-dependent inverse relationship between SHBG and obesity in males
- Limited predictive value of renal biomarkers (albumin, creatinine, iodine)
- Meaningful improvement in explanatory power when combining metabolic markers rather than analyzing them individually

---

## 🏥 Medical Appointment No-Show Analysis (Kaggle Dataset)

A healthcare operations analysis of outpatient appointment attendance behavior, focusing on structural and demographic drivers of no-show risk.

This project examines how scheduling design and patient characteristics interact to influence appointment adherence.

Key analytical components include:
- SQL-based cohort and stratified analysis (DuckDB)
- Feature engineering of appointment lead time
- Interaction analysis across age, wait time, and SMS reminders
- Visualization of risk structure via heatmaps

Key findings:
- Appointment lead time is the strongest predictor of no-show behavior
- Age acts as a risk modifier, with younger patients consistently exhibiting higher no-show rates
- SMS reminders are associated with higher observed risk due to non-random targeting of higher-risk patients
- No-show behavior follows a structured operational gradient rather than isolated demographic effects

---

# 🧭 Analytical Framework

Across projects, I use a consistent healthcare analytics workflow:

- Data ingestion and transformation (ETL pipelines where applicable)
- SQL-based cohort and relational analysis
- Exploratory data analysis with stratified subgrouping
- Regression-based statistical inference (linear and logistic models)
- Explicit interpretation of confounding and observational bias

---

# 🛠️ Tools & Technologies

- SQL (DuckDB, PostgreSQL)
- Python (pandas, numpy, scipy)
- statsmodels (OLS, logistic regression)
- Data visualization (matplotlib, seaborn)

---

# 📌 Project Status

All projects are ongoing and serve as structured demonstrations of healthcare analytics workflows, from raw data processing to interpretable statistical insights.

Future directions include:
- Expanded multivariate modeling
- Causal inference methods for observational healthcare data
- Additional population health datasets (dietary, behavioral, clinical utilization data)

---

# 🔬 Key Skills Demonstrated

- Healthcare data modeling and cohort analysis  
- SQL-based relational data workflows  
- Multivariable regression and stratified analysis  
- Confounding-aware interpretation of observational data  
- Translation of clinical intuition into structured analytics  

---

# 🧠 Notes

These projects are exploratory and observational in nature. Findings describe statistical associations and should not be interpreted as causal relationships.
