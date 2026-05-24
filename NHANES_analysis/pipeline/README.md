# NHANES Biomarker Analysis Pipeline

A reusable epidemiological analysis pipeline for exploring relationships between laboratory biomarkers and chronic disease outcomes using the **NHANES 2017-2020 Pre-Pandemic dataset**.

> **Note:** This pipeline evolved from an initial exploratory analysis (see [exploratory/](../exploratory/)). Methodology was refined during pipeline development — the pipeline analyses should be considered the canonical version.

---

## Background

Built by a clinician transitioning into data analytics, this project combines domain expertise in laboratory medicine and chronic disease with scalable data engineering. The goal was to move beyond one-off analyses toward a system that can answer new epidemiological questions without rewriting code.

NHANES is a CDC program assessing the health and nutritional status of Americans. The 2017-2020 pre-pandemic cycle is one of the most comprehensive population-level health surveys available.

---

## Project Goals

- Build a **reusable, scalable pipeline** for NHANES biomarker analysis
- Enable analysis across **multiple disease states** without hardcoding column names or rewriting code
- Apply **clinical domain knowledge** to cohort definitions, biomarker selection, and exclusion criteria
- Demonstrate end-to-end data engineering: raw ingestion → database design → analysis → results

---

## Dataset

- **Source:** [CDC NHANES 2017-March 2020 Pre-Pandemic](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020)
- **Tables loaded:** 46 laboratory tables (blood and urine), demographics, anthropometry, blood pressure
- **Total biomarkers registered:** 345
- **Format:** XPT files loaded into PostgreSQL

---

## Pipeline Architecture

```
Raw XPT Files
      ↓
raw_table_loading.py     ← automated batch ingestion
      ↓
PostgreSQL (raw schema)
      ↓
biomarker_registry       ← maps NHANES codes → human-readable names + units
      ↓
participant_biomarkers   ← long format: one row per participant per biomarker
participant_demographics ← one row per participant: outcomes + covariates
      ↓
nhanes_analysis.py       ← reusable analysis functions
      ↓
Results
```

### Why a Long Table Design?

Traditional NHANES analyses hardcode column names (e.g. `LBXGH` for HbA1c) — brittle and hard to reuse. This pipeline uses a long table design where:

- Adding a new biomarker = inserting a row in `biomarker_registry`, no schema changes
- Running a new analysis = calling the same functions with different inputs
- All NHANES codes are abstracted away — analysis code only uses human-readable names

---

## Project Structure

```
NHANES_analysis/
├── data/
│   ├── raw/
│   └── processed/
├── exploratory/
│   └── notebooks/
│       ├── 01_data_cleaning/
│       └── 02_analysis/
├── pipeline/
│   ├── nhanes_utils.py                  ← data loading and cleaning utilities
│   ├── nhanes_analysis.py               ← reusable analysis functions
│   ├── diagnosis_config.py              ← disease state definitions
│   ├── raw_table_loading.py             ← automated raw data ingestion
│   ├── notebooks/
│   │   ├── foundational_tables_config.ipynb
│   │   ├── raw_data_upload_pipeline.ipynb
│   │   └── analysis/
│   │       ├── 1.urine_bmi_analysis.ipynb
│   │       ├── 2.blood_carbohydrate_metabolism.ipynb
│   │       └── 3.shbg_bmi_analysis.ipynb
│   └── README.md
└── README.md
```

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

## Raw Data Ingestion (`raw_table_loading.py`)

Automates batch ingestion of NHANES `.xpt` files into PostgreSQL. Eliminates manual file-by-file loading and ensures reproducible database construction.

**Key features:**
- Scans a directory for all `.xpt` files and loads them in one pass
- Assigns semantic table names (e.g. `raw_demographics`, `raw_blood_glycohemoglobin`)
- Preserves original NHANES structure in a raw schema layer
- Modular — supports extension to additional NHANES cycles

```bash
python raw_table_loading.py
```

---

## Analysis Functions (`nhanes_analysis.py`)

All functions share the same interface — pass biomarker names, a disease, and optional cohort filters:

```python
run_cohort_descriptives(biomarkers, disease, engine, filters)
run_biomarker_descriptives(biomarkers, disease, engine, filters)
run_distribution_plots(biomarkers, disease, engine, filters)
run_correlation(biomarkers, disease, engine, method, log_transform, filters)
run_scatter(biomarker, disease, engine, filters)
run_linear_regression(biomarkers, disease, engine, log_transform, filters)
run_logistic_regression(biomarkers, disease, engine, log_transform, filters)
run_quartile_analysis(biomarker, disease, engine, log_transform, filters)
```

### Cohort Filters

```python
filters = {
    "min_age":           18,          # minimum age
    "max_age":           65,          # maximum age
    "age_range":         (22, 49),    # age range (alternative to min/max)
    "sex":               1,           # 1 = Males only, 2 = Females only
    "exclude_diabetes":  True,        # exclude diabetic participants
    "diabetes_criteria": "hba1c_only" # exclusion criterion
}
```

### Disease Configuration (`diagnosis_config.py`)

| Disease | Outcome | Definition |
|---|---|---|
| Obesity | BMI | BMI ≥ 30 kg/m² (WHO) |
| Hypertension | Systolic/Diastolic BP | SBP ≥ 130 OR DBP ≥ 80 mmHg (ACC/AHA 2017) |
| Diabetes | HbA1c | HbA1c ≥ 6.5% (ADA) |

---

## Analyses Conducted

All analyses adjust for age, sex, and race/ethnicity. Biomarkers were log-transformed for correlation and linear regression. Untransformed values used for logistic regression to preserve clinical interpretability of odds ratios.

### Results Summary

| Analysis | Cohort | n | Strongest Biomarker | r | R² | Key OR |
|---|---|---|---|---|---|---|
| [Urine Biomarkers vs BMI](./notebooks/analysis/1.urine_bmi_analysis.ipynb) | Adults ≥ 18 | 2,898 | Creatinine (urine) | 0.163 | 0.063 | 1.004 (NS) |
| [Carb Metabolism vs BMI](./notebooks/analysis/2.blood_carbohydrate_metabolism.ipynb) | Adults ≥ 18, no diabetes | 3,478 | Insulin | 0.556 | 0.329 | 1.118*** |
| [SHBG vs BMI](./notebooks/analysis/3.shbg_bmi_analysis.ipynb) **female cohort analysis in progress**| Males 22–49 | 1,387 | SHBG | -0.352 | 0.155 | 0.947*** |

*** p < 0.001 | NS = not significant

### Key Findings Across Analyses

- **Urine biomarkers** explained only 6.3% of BMI variance — no clinically meaningful association with obesity after adjustment. A valid null finding suggesting these markers reflect renal function, not adiposity.
- **Carbohydrate metabolism markers** were strong predictors of obesity, explaining 32.9% of BMI variance. Insulin was the strongest correlate (r = 0.556). Each 1% increase in HbA1c was associated with 2.26x higher odds of obesity.
- **SHBG** showed a strong inverse association with BMI in younger males (r = -0.352). Each 1 nmol/L increase in SHBG was associated with 5.3% lower odds of obesity, consistent with the known relationship between low SHBG and insulin resistance.

*See individual notebooks for full cohort descriptions, biomarker distributions, and detailed regression outputs.*

---

## Setup

### Requirements
```bash
pip install pandas numpy sqlalchemy psycopg2 pyreadstat \
            requests beautifulsoup4 scipy statsmodels \
            matplotlib seaborn
```

### Database Connection
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:password@localhost:5432/nhanes")
```

### Example Analysis
```python
from nhanes_analysis import (run_cohort_descriptives, run_biomarker_descriptives,
                              run_distribution_plots, run_correlation,
                              run_linear_regression, run_logistic_regression)
from diagnosis_config import DISEASE_CONFIGS

# SHBG vs BMI in males aged 22-49
filters = {"age_range": (22, 49), "sex": 1}

_ = run_cohort_descriptives(["shbg"], "obesity", engine, filters=filters)
_ = run_biomarker_descriptives(["shbg"], "obesity", engine, filters=filters)
run_distribution_plots(["shbg"], "obesity", engine, filters=filters)
run_correlation(["shbg"], "obesity", engine, method="pearson", log_transform=True, filters=filters)
run_linear_regression(["shbg"], "obesity", engine, log_transform=True, filters=filters)
_ = run_logistic_regression(["shbg"], "obesity", engine, log_transform=False, filters=filters)
```

---

## Methodological Notes

- **Log transformation:** Applied for correlation and linear regression to address right skewness. Not applied for logistic regression to preserve clinical interpretability of odds ratios
- **Covariate adjustment:** All models adjust for age, sex, and race/ethnicity. Sex is automatically excluded when a single-sex cohort filter is applied
- **Diabetes exclusion:** Participants excluded based on HbA1c ≥ 6.5% where clinically appropriate
- **Missing data:** Complete case analysis — participants missing any key variable are excluded

---

## Skills Demonstrated

- **Data Engineering** — automated batch ingestion, PostgreSQL schema design, long table architecture, codebook scraping
- **Epidemiological Methods** — cohort definition, exclusion criteria, covariate adjustment, multicollinearity assessment
- **Statistical Analysis** — Pearson correlation, linear and logistic regression, odds ratios with 95% CIs
- **Clinical Domain Knowledge** — biomarker interpretation, disease definitions per ACC/AHA, WHO, and ADA guidelines
- **Python** — reusable function design, SQLAlchemy, pandas, statsmodels, seaborn
- **Reproducibility** — modular, version-controlled codebase separating data, config, and analysis layers

---

## Data Source

Centers for Disease Control and Prevention. National Health and Nutrition Examination Survey 2017-March 2020 Pre-Pandemic Data. Available at: https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020
