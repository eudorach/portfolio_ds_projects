# NHANES Pipeline — Technical Reference

---

## Requirements

```bash
pip install pandas numpy sqlalchemy psycopg2 pyreadstat \
            requests beautifulsoup4 scipy statsmodels \
            matplotlib seaborn scikit-learn
```

Requires a running PostgreSQL instance.

---

## Database Connection

```python
from sqlalchemy import create_engine
engine = create_engine("postgresql://user:password@localhost:5432/nhanes")
```

---

## Project Structure

```
NHANES_analysis/
├── data/
│   ├── raw/                          ← NHANES .xpt files
│   │   └── medical_history/          ← questionnaire .xpt files
│   └── processed/
├── pipeline/
│   ├── figures/                       ← plots for README
│   ├── notebooks/
│   │   ├── raw_data_upload_pipeline.ipynb     ← ingest raw XPT files → PostgreSQL
│   │   ├── foundational_tables_config.ipynb   ← build registries + long tables
│   │   └── analysis/
│   │       ├── 1.urine_bmi_analysis.ipynb
│   │       ├── 2.blood_carbohydrate_metabolism.ipynb
│   │       └── 3.shbg_bmi_analysis.ipynb
│   ├── nhanes_utils.py               ← data loading, ingestion, table builders
│   ├── nhanes_analysis.py            ← reusable analysis functions
│   ├── diagnosis_config.py           ← disease state definitions
│   ├── raw_table_loading.py          ← ingest_folder() implementation
│   ├── README.md
│   └── TECHNICAL.md
```

---

## Pipeline Execution Order

### Step 1 — Ingest Raw XPT Files

```python
from raw_table_loading import ingest_folder

# Lab tables
ingest_folder(path_to_raw, engine, TABLE_NAME_MAP)

# Medical history tables
ingest_folder(path_to_medical_history, engine, med_hx_map)
```

### Step 2 — Build Registries

```python
import nhanes_utils as nu

# Scrape codebooks from CDC and build biomarker_registry
records = []
for table in LAB_TABLES:
    records.extend(nu.scrape_codebook(table, year_start=2017))

# Scrape medical history codebooks and build medhx_registry
records = []
for table in MED_HX_TABLES:
    records.extend(nu.scrape_codebook(table, year_start=2017))
```

### Step 3 — Build Long Tables

```python
# Biomarkers
participant_biomarkers = nu.build_participant_long_table(
    engine,
    registry_table="biomarker_registry",
    id_col="biomarker_id",
    cycle="2017-2020"
)
nu.save_to_postgres(participant_biomarkers, "participant_biomarkers", engine)

# Medical history
participant_medhx = nu.build_participant_long_table(
    engine,
    registry_table="medhx_registry",
    id_col="medhx_id",
    cycle="2017-2020"
)
nu.save_to_postgres(participant_medhx, "participant_medhx", engine)

# Demographics
participant_demographics = nu.build_participant_demographics(engine, cycle="2017-2020")
nu.save_to_postgres(participant_demographics, "participant_demographics", engine)
```

---

## Database Schema

### `biomarker_registry`

| Column | Description |
|---|---|
| `biomarker_id` | Primary key |
| `biomarker_name` | Snake_case human-readable name (e.g. `glycohemoglobin`) |
| `raw_col` | Original NHANES code (e.g. `LBXGH`) |
| `label` | Full description |
| `unit` | Measurement unit (e.g. `%`, `mg/dL`) |
| `source_table` | PostgreSQL raw table name |

### `participant_biomarkers`

| Column | Description |
|---|---|
| `participant_id` | NHANES SEQN identifier |
| `biomarker_id` | Foreign key → `biomarker_registry` |
| `value` | Measured value |
| `cycle` | Survey cycle (e.g. `2017-2020`) |

### `medhx_registry`

| Column | Description |
|---|---|
| `medhx_id` | Primary key |
| `medical_history` | Snake_case human-readable name |
| `raw_col` | Original NHANES code |
| `label` | Full description |
| `source_table` | PostgreSQL raw table name |

### `participant_medhx`

| Column | Description |
|---|---|
| `participant_id` | NHANES SEQN identifier |
| `medhx_id` | Foreign key → `medhx_registry` |
| `value` | Response value (numeric or string) |
| `cycle` | Survey cycle (e.g. `2017-2020`) |

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
| `height_cm` | Height (cm) |
| `weight_kg` | Weight (kg) |
| `systolic_bp` | Systolic blood pressure (mmHg) |
| `diastolic_bp` | Diastolic blood pressure (mmHg) |
| `survey_weight` | NHANES sample weight (WTMECPRP) |
| `psu` | Primary sampling unit |
| `strata` | Sampling strata |
| `poverty_income_ratio` | Income-to-poverty ratio |
| `cycle` | Survey cycle |

---

## Disease Configuration (`diagnosis_config.py`)

| Disease | Outcome | Definition |
|---|---|---|
| `obesity` | BMI | BMI ≥ 30 kg/m² (WHO) |
| `hypertension` | Systolic/Diastolic BP | SBP ≥ 130 OR DBP ≥ 80 mmHg (ACC/AHA 2017) |
| `diabetes` | HbA1c | HbA1c ≥ 6.5% (ADA) |

---

## Analysis Functions (`nhanes_analysis.py`)

All functions share the same core interface:

```python
from nhanes_analysis import *
from diagnosis_config import DISEASE_CONFIGS

filters = {
    "min_age":           18,
    "max_age":           65,
    "age_range":         (22, 49),      # alternative to min/max
    "sex":               1,             # 1 = Males, 2 = Females
    "exclude_diabetes":  True,
    "diabetes_criteria": "hba1c_only"   # "hba1c_only", "glucose_only", "both"
}

covariates = ["age", "sex", "race_ethnicity"]  # default; fully configurable
```

### `load_analysis_data`
Pulls and merges biomarker, demographic, and outcome data into a wide analysis-ready DataFrame.
```python
df = load_analysis_data(biomarkers, disease, engine, filters, covariates)
```

### `run_cohort_descriptives`
Descriptive statistics for continuous and categorical variables in the filtered cohort.
```python
cont_df, sex_df, race_df = run_cohort_descriptives(biomarkers, disease, engine, filters)
```

### `run_biomarker_descriptives`
Descriptive statistics per biomarker with skewness flagging for log transformation.
```python
results_df = run_biomarker_descriptives(biomarkers, disease, engine, filters)
```

### `run_distribution_plots`
Raw and log-transformed distribution plots for each biomarker. Accepts a pre-filtered DataFrame.
```python
run_distribution_plots(biomarkers, disease, engine, filters, df=None)
```

### `run_correlation`
Pearson or Spearman correlation between biomarkers and the outcome variable.
```python
results_df = run_correlation(biomarkers, disease, engine, method="spearman",
                             log_transform=False, filters=None)
```

### `run_scatter`
Scatter plot with regression line for a single biomarker vs outcome.
```python
run_scatter(biomarker, disease, engine, hue_col="sex_label", filters=None)
```

### `run_linear_regression`
OLS linear regression with configurable covariates and optional log transformation.
```python
model = run_linear_regression(biomarkers, disease, engine,
                              log_transform=False, filters=None, covariates=None)
```

### `run_logistic_regression`
Logistic regression returning odds ratios with 95% CIs.
```python
odds_df, model = run_logistic_regression(biomarkers, disease, engine,
                                         log_transform=False, filters=None, covariates=None)
```

### `run_quartile_analysis`
Quartile-based analysis including summary stats, Spearman correlation per quartile, logistic and linear regression with Q1 as reference, bar chart, and forest plot.
```python
summary, quartile_or = run_quartile_analysis(biomarker, disease, engine,
                                             log_transform=False, filters=None, covariates=None)
```

---

## Example: Full Analysis

```python
from nhanes_analysis import *
from diagnosis_config import DISEASE_CONFIGS

biomarkers = ["shbg"]
disease    = "obesity"
filters    = {"age_range": (22, 49), "sex": 1}

# Descriptives
run_cohort_descriptives(biomarkers, disease, engine, filters)
run_biomarker_descriptives(biomarkers, disease, engine, filters)
run_distribution_plots(biomarkers, disease, engine, filters)

# Correlation
run_correlation(biomarkers, disease, engine,
                method="pearson", log_transform=True, filters=filters)

# Regression
run_linear_regression(biomarkers, disease, engine,
                      log_transform=True, filters=filters)

run_logistic_regression(biomarkers, disease, engine,
                        log_transform=False, filters=filters)

# Quartile analysis
run_quartile_analysis(biomarkers[0], disease, engine,
                      log_transform=True, filters=filters)
```

---

## Data Source

Centers for Disease Control and Prevention. National Health and Nutrition Examination Survey 2017–March 2020 Pre-Pandemic Data.
https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?cycle=2017-2020
