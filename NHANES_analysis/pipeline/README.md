# NHANES Biomarker Analysis Pipeline

A reusable epidemiological analysis pipeline for exploring relationships between laboratory biomarkers and chronic disease outcomes using the **NHANES 2017-2020 Pre-Pandemic dataset**.

---

## Background

This project was built by a clinician transitioning into data analytics, combining domain expertise in laboratory medicine and chronic disease with a scalable data engineering approach. The goal was to move beyond one-off analyses toward a system that can answer new epidemiological questions without rewriting code.

The National Health and Nutrition Examination Survey (NHANES) is a CDC program that assesses the health and nutritional status of adults and children in the United States. The 2017-2020 pre-pandemic cycle is a combined dataset representing one of the most comprehensive population-level health surveys available.

---

## Project Goals

- Build a **reusable, scalable pipeline** for NHANES biomarker analysis
- Enable analysis across **multiple disease states** (obesity, hypertension, diabetes) without hardcoding column names or rewriting analysis code
- Apply **clinical domain knowledge** to make methodologically sound decisions (cohort definitions, biomarker selection, exclusion criteria)
- Demonstrate end-to-end data engineering: raw data ingestion → database design → analysis → results

---

## Dataset

- **Source:** [CDC NHANES 2017-March 2020 Pre-Pandemic](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020)
- **Tables loaded:** 46 laboratory tables (blood and urine), demographics, anthropometry, blood pressure
- **Total biomarkers registered:** 201
- **Format:** XPT files loaded into PostgreSQL

---

## Pipeline Architecture

```
Raw XPT Files
      ↓
PostgreSQL (raw schema)
      ↓
biomarker_registry       ← maps NHANES codes to human-readable names + units
      ↓
participant_biomarkers   ← long format: one row per participant per biomarker
participant_demographics ← one row per participant: outcomes + covariates
      ↓
nhanes_analysis.py       ← reusable analysis functions
      ↓
Results
```

### Why a Long Table Design?

Traditional NHANES analyses hardcode column names (e.g. `LBXGH` for HbA1c) making code brittle and hard to reuse. This pipeline uses a **long table design** where:

- Adding a new biomarker = inserting a row in `biomarker_registry`, no schema changes
- Running a new analysis = calling the same functions with different inputs
- All NHANES codes are abstracted away — analysis code only uses human-readable names

---

## Database Schema

### `biomarker_registry`
| Column | Description |
|---|---|
| `biomarker_id` | Primary key |
| `biomarker_name` | Human-readable snake_case name (e.g. `glycohemoglobin`) |
| `raw_col` | Original NHANES column code (e.g. `LBXGH`) |
| `label` | Full description |
| `unit` | Measurement unit (e.g. `%`, `mg/dL`) |
| `source_table` | PostgreSQL raw table name |

### `participant_biomarkers`
| Column | Description |
|---|---|
| `participant_id` | NHANES SEQN identifier |
| `biomarker_id` | Foreign key → `biomarker_registry` |
| `value` | Measured value |
| `cycle` | Survey cycle (2017-2020) |

### `participant_demographics`
| Column | Description |
|---|---|
| `participant_id` | NHANES SEQN identifier |
| `age` | Age in years |
| `sex` | 1 = Male, 2 = Female |
| `sex_label` | Male / Female |
| `race_ethnicity` | Numeric code |
| `race_ethnicity_label` | e.g. Non-Hispanic White |
| `bmi` | Body mass index (kg/m²) |
| `waist_cm` | Waist circumference (cm) |
| `systolic_bp` | Systolic blood pressure (mmHg) |
| `diastolic_bp` | Diastolic blood pressure (mmHg) |
| `survey_weight` | NHANES sample weight |

---

## Analysis Functions (`nhanes_analysis.py`)

All functions follow the same interface — pass biomarker names, a disease, and optional cohort filters:

```python
run_cohort_descriptives(biomarkers, disease, engine, filters)
run_biomarker_descriptives(biomarkers, disease, engine, filters)
run_distribution_plots(biomarkers, disease, engine, filters)
run_correlation(biomarkers, disease, engine, method, log_transform, filters)
run_scatter(biomarker, disease, engine, filters)
run_linear_regression(biomarkers, disease, engine, log_transform, filters)
run_logistic_regression(biomarkers, disease, engine, log_transform, filters)
```

### Cohort Filters
Filters are passed as a dictionary at analysis time — no config changes needed:

```python
filters = {
    "min_age":           18,            # minimum age
    "max_age":           65,            # maximum age
    "age_range":         (22, 49),      # age range (alternative to min/max)
    "sex":               1,             # 1 = Males only, 2 = Females only
    "exclude_diabetes":  True,          # exclude diabetic participants
    "diabetes_criteria": "hba1c_only"   # exclusion criterion
}
```

### Log Transformation Policy
Biomarkers were natural log-transformed for correlation and linear regression to address right skewness and meet normality assumptions. For logistic regression, untransformed values were retained to facilitate clinically interpretable odds ratios — allowing direct interpretation per unit change in the original measurement scale.

### Disease Configuration (`disease_config.py`)
Diseases are defined once and reused across all analyses:

| Disease | Outcome | Definition |
|---|---|---|
| Obesity | BMI | BMI ≥ 30 kg/m² (WHO) |
| Hypertension | Systolic/Diastolic BP | SBP ≥ 130 OR DBP ≥ 80 mmHg (ACC/AHA 2017) |
| Diabetes | HbA1c | HbA1c ≥ 6.5% (ADA) |

---

## Analyses Conducted

---

### 1. Urine Biomarkers vs BMI

**Cohort:** Adults ≥ 18 years (n = 2,898)  
**Biomarkers:** Urine albumin, urine creatinine, urine iodine  
**Covariates:** Age, sex, race/ethnicity  

#### Cohort Description
| Variable | Mean ± SD | Median (IQR) |
|---|---|---|
| Age (years) | 49.62 ± 18.25 | 51.0 (34.0–64.0) |
| BMI (kg/m²) | 29.75 ± 7.45 | 28.5 (24.5–33.6) |
| Systolic BP (mmHg) | 124.80 ± 19.92 | 122.0 (110.0–136.0) |
| Diastolic BP (mmHg) | 75.01 ± 11.69 | 74.0 (67.0–82.0) |

Sex: Female 51.1%, Male 48.9%

#### Biomarker Descriptives
| Biomarker | Unit | Mean | SD | Median | Skewness | Log transform? |
|---|---|---|---|---|---|---|
| Albumin (urine) | µg/mL | 54.71 | 399.31 | 8.70 | 22.28 | Yes |
| Creatinine (urine) | mg/dL | 127.99 | 84.39 | 111.00 | 1.26 | Yes |
| Iodine (urine) | µg/L | 238.29 | 812.82 | 123.65 | 19.30 | Yes |

#### Correlation Results (Pearson, log-transformed)
| Biomarker | r | p-value | Significant |
|---|---|---|---|
| Creatinine (urine) | 0.163 | < 0.001 | Yes |
| Albumin (urine) | 0.152 | < 0.001 | Yes |
| Iodine (urine) | 0.085 | < 0.001 | Yes |

#### Linear Regression (outcome: BMI, log-transformed, R² = 0.053)
| Predictor | Coefficient | p-value |
|---|---|---|
| Creatinine (urine) | 0.017 | < 0.001 |
| Albumin (urine) | 0.001 | 0.104 |
| Iodine (urine) | -0.0002 | 0.357 |
| Age | 0.037 | < 0.001 |
| Sex | 1.821 | < 0.001 |
| Race/ethnicity | -0.488 | < 0.001 |

#### Logistic Regression (outcome: Obesity yes/no, untransformed)
| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| Creatinine (urine) | 1.004 | 1.003–1.005 | < 0.001 |
| Albumin (urine) | 1.000 | 1.000–1.000 | 0.275 |
| Iodine (urine) | 1.000 | 1.000–1.000 | 0.588 |
| Age | 1.007 | 1.002–1.011 | 0.003 |
| Sex | 1.587 | 1.356–1.857 | < 0.001 |
| Race/ethnicity | 0.863 | 0.821–0.906 | < 0.001 |

#### Key Findings
Urine biomarkers showed no clinically meaningful association with obesity after adjusting for age, sex, and race/ethnicity (R² = 0.053). Only creatinine reached statistical significance, likely reflecting its known association with muscle mass rather than adiposity. Albumin and iodine were not significant predictors of obesity status. These findings suggest urine biomarkers measured in this panel reflect renal function rather than adiposity.

---

### 2. Carbohydrate Metabolism vs BMI

**Cohort:** Adults ≥ 18 years, excluding diabetes (HbA1c < 6.5%) (n = 3,478)  
**Biomarkers:** Fasting glucose, insulin, glycohemoglobin (HbA1c)  
**Covariates:** Age, sex, race/ethnicity  
**Note:** Fasting glucose excluded from regression models due to multicollinearity with HbA1c.

#### Cohort Description
| Variable | Mean ± SD | Median (IQR) |
|---|---|---|
| Age (years) | 47.76 ± 18.23 | 47.0 (32.0–62.0) |
| BMI (kg/m²) | 29.28 ± 7.37 | 28.0 (24.2–32.8) |
| Systolic BP (mmHg) | 122.40 ± 18.65 | 119.0 (109.0–132.0) |
| Diastolic BP (mmHg) | 74.55 ± 11.64 | 73.0 (67.0–82.0) |

Sex: Female 52.1%, Male 47.9%

#### Biomarker Descriptives
| Biomarker | Unit | Mean | SD | Median | Skewness | Log transform? |
|---|---|---|---|---|---|---|
| Fasting glucose | mg/dL | 102.77 | 12.98 | 101.00 | 1.54 | Yes |
| Insulin | µU/mL | 12.96 | 15.92 | 9.41 | 12.36 | Yes |
| Glycohemoglobin | % | 5.50 | 0.40 | 5.50 | -0.14 | No |

#### Correlation Results (Pearson, log-transformed)
| Biomarker | r | p-value | Significant |
|---|---|---|---|
| Insulin | 0.556 | < 0.001 | Yes |
| Fasting Glucose | 0.233 | < 0.001 | Yes |
| Glycohemoglobin | 0.225 | < 0.001 | Yes |

#### Linear Regression (outcome: BMI, log-transformed, R² = 0.329)
| Predictor | Coefficient | p-value |
|---|---|---|
| Glycohemoglobin | 11.755 | < 0.001 |
| Insulin | 5.194 | < 0.001 |
| Age | -0.011 | 0.088 |
| Sex | 1.286 | < 0.001 |
| Race/ethnicity | -0.264 | < 0.001 |

#### Logistic Regression (outcome: Obesity yes/no, untransformed)
| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| Glycohemoglobin | 2.259 | 1.795–2.844 | < 0.001 |
| Insulin | 1.118 | 1.105–1.130 | < 0.001 |
| Age | 0.994 | 0.989–0.999 | 0.012 |
| Sex | 1.582 | 1.353–1.849 | < 0.001 |
| Race/ethnicity | 0.888 | 0.846–0.933 | < 0.001 |

#### Key Findings
Carbohydrate metabolism markers showed meaningful associations with obesity, explaining 32.9% of BMI variance after log transformation. Insulin was the strongest correlate of BMI (r = 0.556), consistent with its central role in insulin resistance and adiposity. Each 1% increase in HbA1c was associated with 2.26x higher odds of obesity (OR = 2.26, 95% CI: 1.80–2.84), and each 1 µU/mL increase in insulin was associated with 12% higher odds of obesity (OR = 1.12). Females had 58% higher odds of obesity compared to males (OR = 1.58), consistent with known sex differences in body fat distribution.

---

### 3. SHBG vs BMI (Males, Ages 22–49)

**Cohort:** Males aged 22–49 years (n = 1,387)  
**Biomarker:** Sex hormone-binding globulin (SHBG)  
**Covariates:** Age, race/ethnicity (sex excluded — male-only cohort)  

#### Cohort Description
| Variable | Mean ± SD | Median (IQR) |
|---|---|---|
| Age (years) | 35.80 ± 8.21 | 36.0 (29.0–43.0) |
| BMI (kg/m²) | 29.72 ± 6.98 | 28.5 (25.0–33.3) |
| Systolic BP (mmHg) | 121.87 ± 13.66 | 120.0 (113.0–129.0) |
| Diastolic BP (mmHg) | 76.30 ± 11.31 | 76.0 (68.0–83.0) |

#### Biomarker Descriptives
| Biomarker | Unit | Mean | SD | Median | Skewness | Log transform? |
|---|---|---|---|---|---|---|
| SHBG | nmol/L | 30.24 | 14.66 | 27.42 | 1.56 | Yes |

#### Correlation Results (Pearson, log-transformed)
| Biomarker | r | p-value | Significant |
|---|---|---|---|
| SHBG | -0.352 | < 0.001 | Yes |

#### Linear Regression (outcome: BMI, log-transformed, R² = 0.155)
| Predictor | Coefficient | p-value |
|---|---|---|
| SHBG | -5.422 | < 0.001 |
| Age | 0.121 | < 0.001 |
| Race/ethnicity | -0.452 | < 0.001 |

#### Logistic Regression (outcome: Obesity yes/no, untransformed)
| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| SHBG | 0.947 | 0.937–0.957 | < 0.001 |
| Age | 1.032 | 1.018–1.047 | < 0.001 |
| Race/ethnicity | 0.853 | 0.798–0.913 | < 0.001 |

#### Key Findings
SHBG showed a strong inverse association with BMI in males aged 22–49 (r = -0.352). Each 1 nmol/L increase in SHBG was associated with 5.3% lower odds of obesity (OR = 0.947), consistent with the known relationship between low SHBG and insulin resistance and metabolic syndrome in males. Age was positively associated with obesity odds in this cohort (OR = 1.032), reflecting increasing metabolic risk with age even in younger males.

---

## Project Structure

```
NHANES_analysis/
├── exploratory/                         ← initial one-off analyses (starting point)
│   └── notebooks/
└── pipeline/                            ← refined, reusable system (this project)
    ├── nhanes_utils.py                  ← data loading and cleaning utilities
    ├── nhanes_analysis.py               ← reusable analysis functions
    ├── disease_config.py                ← disease state definitions
    ├── notebooks/
    │   ├── 01_data_loading.ipynb
    │   ├── 02_registry.ipynb
    │   ├── 03_long_tables.ipynb
    │   └── analysis/
    │       ├── urine_biomarkers_bmi.ipynb
    │       ├── carb_metabolism_bmi.ipynb
    │       └── shbg_males_bmi.ipynb
    └── README.md
```

---

## Setup

### Requirements
```
pip install pandas numpy sqlalchemy psycopg2 pyreadstat
            requests beautifulsoup4 scipy statsmodels
            matplotlib seaborn
```

### Database
Requires a running PostgreSQL instance. Update your connection string:
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:password@localhost:5432/nhanes")
```

### Running an Analysis
```python
from nhanes_analysis import (run_cohort_descriptives, run_biomarker_descriptives,
                              run_distribution_plots, run_correlation,
                              run_linear_regression, run_logistic_regression)
from disease_config import DISEASE_CONFIGS

# Example: SHBG vs BMI in males aged 22-49
filters = {"age_range": (22, 49), "sex": 1}

_ = run_cohort_descriptives(["shbg"], "obesity", engine, filters=filters)
_ = run_biomarker_descriptives(["shbg"], "obesity", engine, filters=filters)
run_distribution_plots(["shbg"], "obesity", engine, filters=filters)

run_correlation(["shbg"], "obesity", engine, method="pearson",
                log_transform=True, filters=filters)

run_linear_regression(["shbg"], "obesity", engine,
                      log_transform=True, filters=filters)

_ = run_logistic_regression(["shbg"], "obesity", engine,
                             log_transform=False, filters=filters)
```

---

## Methodological Notes

- **Log transformation:** Applied for correlation and linear regression to address right skewness. Not applied for logistic regression to preserve clinical interpretability of odds ratios
- **Covariate adjustment:** All models adjust for age, sex, and race/ethnicity. Sex is automatically excluded from models when a single-sex cohort filter is applied
- **Diabetes exclusion:** Participants excluded based on HbA1c ≥ 6.5% where clinically appropriate
- **Missing data:** Complete case analysis — participants missing any key variable are excluded

---

## Skills Demonstrated

- **Data Engineering** — PostgreSQL schema design, long table architecture, automated codebook scraping
- **Epidemiological Methods** — cohort definition, exclusion criteria, covariate adjustment, multicollinearity assessment
- **Statistical Analysis** — Pearson correlation, linear and logistic regression, odds ratios with 95% CIs
- **Clinical Domain Knowledge** — biomarker interpretation, disease definitions based on ACC/AHA, WHO, and ADA clinical guidelines
- **Python** — reusable function design, SQLAlchemy, pandas, statsmodels, seaborn
- **Reproducibility** — version-controlled, modular codebase that separates data, config, and analysis layers

---

## Data Source

Centers for Disease Control and Prevention. National Health and Nutrition Examination Survey 2017-March 2020 Pre-Pandemic Data. Available at: https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020
