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
run_correlation(biomarkers, disease, engine, method, log_transform, filters)
run_scatter(biomarker, disease, engine, filters)
run_linear_regression(biomarkers, disease, engine, log_transform, filters)
run_logistic_regression(biomarkers, disease, engine, log_transform, filters)
```

### Cohort Filters
Filters are passed as a dictionary at analysis time — no config changes needed:

```python
filters = {
    "min_age":           18,            # adults only
    "exclude_diabetes":  True,          # exclude diabetic participants
    "diabetes_criteria": "hba1c_only"   # use HbA1c >= 6.5% as exclusion criterion
}
```

### Disease Configuration (`disease_config.py`)
Diseases are defined once and reused across all analyses:

| Disease | Outcome | Definition |
|---|---|---|
| Obesity | BMI | BMI ≥ 30 kg/m² (WHO) |
| Hypertension | Systolic/Diastolic BP | SBP ≥ 130 OR DBP ≥ 80 mmHg (ACC/AHA 2017) |
| Diabetes | HbA1c | HbA1c ≥ 6.5% (ADA) |

---

## Analyses Conducted

### 1. Urine Biomarkers vs BMI
**Cohort:** Adults ≥ 18 years (n = 2,846)  
**Biomarkers:** Urine albumin, urine creatinine, urine iodine  
**Methods:** Pearson correlation (log-transformed), linear regression, logistic regression  
**Covariates:** Age, sex, race/ethnicity  

#### Correlation Results
| Biomarker | r | p-value | Significant |
|---|---|---|---|
| Urine Creatinine | 0.163 | < 0.001 | Yes |
| Urine Albumin | 0.152 | < 0.001 | Yes |
| Urine Iodine | 0.085 | < 0.001 | Yes |

#### Linear Regression (outcome: BMI, R² = 0.053)
| Predictor | Coefficient | p-value |
|---|---|---|
| Creatinine (urine) | 0.017 | < 0.001 |
| Albumin (urine) | 0.001 | 0.104 |
| Iodine (urine) | -0.0002 | 0.357 |
| Age | 0.037 | < 0.001 |
| Sex | 1.821 | < 0.001 |
| Race/ethnicity | -0.488 | < 0.001 |

#### Logistic Regression (outcome: Obesity yes/no)
| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| Creatinine (urine) | 1.004 | 1.003–1.005 | < 0.001 |
| Albumin (urine) | 1.000 | 1.000–1.000 | 0.275 |
| Iodine (urine) | 1.000 | 1.000–1.000 | 0.588 |
| Age | 1.007 | 1.002–1.011 | 0.003 |
| Sex | 1.587 | 1.356–1.857 | < 0.001 |
| Race/ethnicity | 0.863 | 0.821–0.906 | < 0.001 |

#### Key Findings
Urine biomarkers showed no clinically meaningful association with obesity after adjusting for age, sex, and race/ethnicity (R² = 0.053). Only creatinine reached statistical significance, likely reflecting its known association with muscle mass rather than adiposity. These findings suggest urine biomarkers measured in this panel are not strong predictors of obesity status.

---

### 2. Carbohydrate Metabolism vs BMI
**Cohort:** Adults ≥ 18 years, excluding diabetes (HbA1c < 6.5%) (n = 3,423)  
**Biomarkers:** Fasting glucose, insulin, glycohemoglobin (HbA1c)  
**Methods:** Pearson correlation, linear regression, logistic regression  
**Covariates:** Age, sex, race/ethnicity  
**Note:** Fasting glucose was excluded from regression models due to multicollinearity with HbA1c.

#### Correlation Results
| Biomarker | r | p-value | Significant |
|---|---|---|---|
| Insulin | 0.364 | < 0.001 | Yes |
| Fasting Glucose | 0.232 | < 0.001 | Yes |
| Glycohemoglobin (HbA1c) | 0.228 | < 0.001 | Yes |

#### Linear Regression (outcome: BMI, R² = 0.185)
| Predictor | Coefficient | p-value |
|---|---|---|
| Glycohemoglobin | 3.950 | < 0.001 |
| Insulin | 0.152 | < 0.001 |
| Age | -0.030 | < 0.001 |
| Sex | 1.515 | < 0.001 |
| Race/ethnicity | -0.433 | < 0.001 |

#### Logistic Regression (outcome: Obesity yes/no)
| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| Glycohemoglobin | 2.259 | 1.795–2.844 | < 0.001 |
| Insulin | 1.118 | 1.105–1.130 | < 0.001 |
| Age | 0.994 | 0.989–0.999 | 0.012 |
| Sex | 1.582 | 1.353–1.849 | < 0.001 |
| Race/ethnicity | 0.888 | 0.846–0.933 | < 0.001 |

#### Key Findings
Carbohydrate metabolism markers showed meaningful associations with obesity, explaining 18.5% of BMI variance. Insulin was the strongest correlate of BMI (r = 0.364), consistent with its role in insulin resistance and adiposity. Each 1% increase in HbA1c was associated with 2.26x higher odds of obesity (OR = 2.26, 95% CI: 1.80–2.84), and each 1 µU/mL increase in insulin was associated with 12% higher odds of obesity (OR = 1.12). Females had 58% higher odds of obesity compared to males (OR = 1.58), consistent with known sex differences in adiposity.

---

## Project Structure

```
NHANES_analysis/
├── exploratory/                         ← original one-off analyses
│   └── notebooks/
└── pipeline/                            ← reusable system (this project)
    ├── nhanes_utils.py                  ← data loading and cleaning utilities
    ├── nhanes_analysis.py               ← reusable analysis functions
    ├── disease_config.py                ← disease state definitions
    ├── notebooks/
    │   ├── 01_data_loading.ipynb
    │   ├── 02_registry.ipynb
    │   ├── 03_long_tables.ipynb
    │   └── analysis/
    │       ├── urine_biomarkers_bmi.ipynb
    │       └── carb_metabolism_bmi.ipynb
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
from nhanes_analysis import run_correlation, run_linear_regression, run_logistic_regression
from disease_config import DISEASE_CONFIGS

# Carbohydrate metabolism vs BMI in adults without diabetes
filters = {"min_age": 18, "exclude_diabetes": True, "diabetes_criteria": "hba1c_only"}

run_correlation(
    biomarkers=["fasting_glucose", "glycohemoglobin", "insulin"],
    disease="obesity",
    engine=engine,
    method="pearson",
    filters=filters
)

run_linear_regression(
    biomarkers=["glycohemoglobin", "insulin"],
    disease="obesity",
    engine=engine,
    filters=filters
)

run_logistic_regression(
    biomarkers=["glycohemoglobin", "insulin"],
    disease="obesity",
    engine=engine,
    filters=filters
)
```

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
