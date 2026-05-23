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

## 📁 Projects

### 🧬 NHANES Biomarker Analysis Pipeline (2017–2020)

A reusable epidemiological analysis pipeline for exploring relationships between laboratory biomarkers and chronic disease outcomes using the NHANES 2017-2020 pre-pandemic dataset.

This project evolved from an initial exploratory analysis into a fully engineered, scalable pipeline — reflecting a deliberate shift from one-off notebooks toward production-grade, reusable infrastructure.

**Pipeline architecture includes:**
- Automated codebook scraping to build a 201-biomarker registry from CDC documentation
- Long-table PostgreSQL schema design for scalable biomarker storage
- Reusable analysis functions supporting any biomarker/disease combination without code changes
- Flexible cohort filter system for age, disease exclusions, and subgroup definitions

**Analyses conducted:**
- Urine biomarkers (albumin, creatinine, iodine) vs BMI — adults ≥ 18 (n = 2,846)
- Carbohydrate metabolism markers (HbA1c, insulin, fasting glucose) vs BMI — adults ≥ 18 without diabetes (n = 3,423)

**Key findings:**
- Insulin was the strongest correlate of BMI among carbohydrate metabolism markers (r = 0.364), consistent with insulin resistance in obesity
- Each 1% increase in HbA1c was associated with 2.26x higher odds of obesity (OR = 2.26, 95% CI: 1.80–2.84)
- Carbohydrate metabolism markers explained 18.5% of BMI variance vs 5.3% for urine biomarkers
- Urine biomarkers showed no clinically meaningful association with obesity after multivariable adjustment — a valid null finding suggesting these markers reflect renal function rather than adiposity

📂 [Exploratory Analysis](./NHANES_analysis/exploratory/) | [Pipeline](./NHANES_analysis/pipeline/)

---

### 🏥 Medical Appointment No-Show Analysis (Kaggle Dataset)

A healthcare operations analysis of outpatient appointment attendance behavior, focusing on structural and demographic drivers of no-show risk.

This project examines how scheduling design and patient characteristics interact to influence appointment adherence.

**Key analytical components include:**
- SQL-based cohort and stratified analysis (DuckDB)
- Feature engineering of appointment lead time
- Interaction analysis across age, wait time, and SMS reminders
- Visualization of risk structure via heatmaps

**Key findings:**
- Appointment lead time is the strongest predictor of no-show behavior
- Age acts as a risk modifier, with younger patients consistently exhibiting higher no-show rates
- SMS reminders are associated with higher observed risk due to non-random targeting of higher-risk patients
- No-show behavior follows a structured operational gradient rather than isolated demographic effects

---

## 🧭 Analytical Framework

Across projects, I use a consistent healthcare analytics workflow:

1. Data ingestion and transformation (ETL pipelines where applicable)
2. SQL-based cohort and relational analysis
3. Exploratory data analysis with stratified subgrouping
4. Regression-based statistical inference (linear and logistic models)
5. Explicit interpretation of confounding and observational bias

---

## 🛠️ Tools & Technologies

- **Databases:** PostgreSQL, DuckDB
- **Python:** pandas, numpy, scipy, statsmodels, seaborn, matplotlib
- **Data engineering:** SQLAlchemy, pyreadstat, BeautifulSoup (web scraping)
- **Statistical methods:** Pearson/Spearman correlation, OLS regression, logistic regression, odds ratios

---

## 📌 Project Status

All projects are ongoing and serve as structured demonstrations of healthcare analytics workflows, from raw data processing to interpretable statistical insights.

**Future directions include:**
- CKD and metabolic syndrome analysis using the existing pipeline
- Hypertension biomarker analysis
- Survey-weighted analyses for population-level inference
- Causal inference methods for observational healthcare data
- Additional population health datasets (dietary, behavioral, clinical utilization)

---

## 🔬 Key Skills Demonstrated

- **Data engineering** — pipeline design, long-table schema, automated registry building
- **Epidemiological methods** — cohort definition, exclusion criteria, covariate adjustment
- **Statistical analysis** — correlation, linear and logistic regression, odds ratios with 95% CIs
- **Clinical domain knowledge** — biomarker interpretation, disease definitions from ACC/AHA, WHO, and ADA guidelines
- **Reproducibility** — modular, version-controlled codebase separating data, config, and analysis layers

---

## 🧠 Notes

These projects are exploratory and observational in nature. Findings describe statistical associations and should not be interpreted as causal relationships.
