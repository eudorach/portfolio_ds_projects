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
run_linear_regression(biomarkers, disease, engine, filters)
run_logistic_regression(biomarkers, disease, engine, filters)
```

### Cohort Filters
Filters are passed as a dictionary at analysis time — no config changes needed:

```python
filters = {
    "min_age":          18,       # adults only
    "exclude_diabetes": True,     # exclude HbA1c >= 6.5% or fasting glucose >= 126 mg/dL
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
**Cohort:** Adults ≥ 18 years  
**Biomarkers:** Urine albumin, urine creatinine, urine iodine  
**Methods:** Pearson correlation, linear regression, logistic regression  
**Covariates:** Age, sex, race/ethnicity  

### 2. Carbohydrate Metabolism vs BMI
**Cohort:** Adults ≥ 18 years, excluding diabetes (HbA1c < 6.5% AND fasting glucose < 126 mg/dL)  
**Biomarkers:** Fasting glucose, insulin, glycohemoglobin  
**Methods:** Pearson correlation, linear regression, logistic regression  
**Covariates:** Age, sex, race/ethnicity  
**Key findings:**
- Insulin showed the strongest positive correlation with BMI (r = 0.30)
- Glycohemoglobin and fasting glucose showed moderate positive correlations (r ≈ 0.20)
- All associations remained significant after adjusting for age, sex, and race/ethnicity

---

## Project Structure

```
NHANES_analysis/
│
├── notebooks/
│   ├── 01_data_loading/
│   │   └── nhanes_data_load.ipynb       # Load XPT files → PostgreSQL
│   ├── 02_registry/
│   │   └── nhanes_scraper.ipynb         # Build biomarker_registry
│   ├── 03_long_tables/
│   │   └── nhanes_long_tables.ipynb     # Build participant_biomarkers
│   └── 04_analysis/
│       ├── urine_biomarkers_bmi.ipynb
│       └── carb_metabolism_bmi.ipynb
│
├── nhanes_utils.py                      # Data loading and cleaning utilities
├── nhanes_analysis.py                   # Reusable analysis functions
├── disease_config.py                    # Disease state definitions
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
from nhanes_analysis import run_correlation, run_linear_regression
from disease_config import DISEASE_CONFIGS

# Example: carbohydrate biomarkers vs BMI in adults without diabetes
run_correlation(
    biomarkers=["fasting_glucose", "glycohemoglobin", "insulin"],
    disease="obesity",
    engine=engine,
    method="pearson",
    filters={"min_age": 18, "exclude_diabetes": True}
)
```

---

## Skills Demonstrated

- **Data Engineering** — PostgreSQL schema design, long table architecture, automated codebook scraping
- **Epidemiological Methods** — cohort definition, exclusion criteria, covariate adjustment
- **Statistical Analysis** — correlation, linear and logistic regression, odds ratios
- **Clinical Domain Knowledge** — biomarker interpretation, disease definitions based on clinical guidelines
- **Python** — reusable function design, SQLAlchemy, pandas, statsmodels, seaborn
- **Reproducibility** — version-controlled, modular codebase that separates data, config, and analysis

---

## Data Source

Centers for Disease Control and Prevention. National Health and Nutrition Examination Survey 2017-March 2020 Pre-Pandemic Data. Available at: https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020
