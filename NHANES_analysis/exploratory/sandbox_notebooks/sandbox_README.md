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

Analysis evolved from an initial predictive modeling approach to an exploratory design based on observed correlation strengths

---

## Data Source
- NHANES 2017–2020 cycles (CDC)
- Public health survey dataset
- Data structured into a PostgreSQL relational database

---

## [Data Processing Pipeline](./notebooks/01_data_cleaning)
Raw NHANES datasets were processed using Python-based [ETL pipelines](./notebooks/01_data_cleaning/nhanes_utils.py).

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

#### Carbohydrate Metabolism
- Clinical Motivation
  
Insulin resistance and dysglycemia are central to obesity-related metabolic dysfunction. This analysis evaluates whether biomarkers of glucose regulation are independently associated with BMI and whether insulin provides stronger explanatory signal than downstream glycemic markers (fasting glucose and HbA1c).

- Cohort
  
U.S. adults from NHANES with complete data on BMI, fasting glucose, fasting insulin, HbA1c, age, sex, and race/ethnicity (n = 3,146).
Participants with missing metabolic biomarker data were excluded to ensure comparability across models.

- Approach
  
Pearson correlations between BMI and metabolic biomarkers (overall and sex-stratified)
Multivariable OLS regression with BMI as the outcome
Models adjusted for age, sex, and race/ethnicity
Separate univariate and multivariable models for each biomarker
Joint models including insulin, glucose, and HbA1c to assess independent effects
Effect heterogeneity assessed via sex-stratified correlations

- Findings
  
Fasting insulin showed the strongest and most consistent association with BMI (r = 0.41 overall), with minimal variation across sex (males: r = 0.42; females: r = 0.43).

Fasting glucose demonstrated a weaker association with BMI (r = 0.23 overall), with slightly higher correlation in females (r = 0.26) compared to males (r = 0.23).

HbA1c showed a modest overall association with BMI (r = 0.21) but demonstrated notable sex differences, with a stronger association in females (r = 0.26) than males (r = 0.15).

In adjusted regression models, fasting insulin remained the strongest independent predictor of BMI. HbA1c and fasting glucose remained statistically significant but were attenuated when modeled jointly with insulin. The combined model improved explanatory power (R² ≈ 0.24), indicating partial independence across metabolic pathways.

- Limitations & Next Steps
  
This is a cross-sectional analysis; causality cannot be inferred. Reverse causation is plausible, as increased adiposity may contribute to elevated insulin and downstream glycemic dysregulation.

Next steps include standardization of predictors to enable effect size comparison, formal testing of sex interactions (particularly HbA1c × sex), and evaluation of potential non-linear relationships between insulin and BMI.

→ [Full analysis notebook](./notebooks/02_analysis/4.blood_lab_carbohydrate_metabolism.ipynb)

- [Lipid panel](./notebooks/02_analysis/7_blood_lab_lipidpanel.ipynb) (in progress)

---

### 3. Sex Hormones

#### Sex Hormone Binding Globulin
- Clinical Motivation
  
SHBG is a key regulator of androgen and estrogen bioavailability. This analysis examines whether SHBG levels are independently associated with obesity after adjusting for key demographic covariates.

- Cohort
  
Adult males aged 20–49 (n = 1,447). This subgroup was selected to reduce hormonal variability introduced by female menstrual cycle fluctuations and age-related hormonal decline in older males.

- Approach
  
SHBG categorized into quartiles to capture potential non-linear relationships
Obesity defined as BMI ≥ 30 kg/m²
Multivariable logistic regression adjusted for age and race/ethnicity
Adjusted predicted probabilities derived holding covariates at mean values

- Findings
  
Each increase in SHBG quartile corresponded to significantly lower odds of obesity (OR = 0.50, 95% CI: 0.45–0.56, p < 0.001), with a monotonic decrease in adjusted predicted obesity probability across quartiles. The association was consistent in both unadjusted and adjusted models.

- Limitations & Next Steps
  
Cross-sectional design precludes causal inference. Reverse causation remains plausible. Analysis is being extended to a female cohort with appropriate hormonal covariates.

→ [Full analysis notebook](./notebooks/02_analysis/7_blood_lab_SHBG.ipynb)
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
