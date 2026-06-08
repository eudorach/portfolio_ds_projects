# Portfolio — Clinical Data Analytics & Real-World Evidence

I'm a clinician building toward clinical data analytics, with a focus on real-world evidence and population health. These projects sit at the intersection of clinical domain knowledge and data engineering.

---

## Featured Project: NHANES Biomarker Analysis Pipeline

**A reusable, registry-based epidemiological analysis pipeline built on NHANES 2017–2020 pre-pandemic data.**

39 laboratory tables · 347 biomarkers · 11 medical history modules · 2,093,413 biomarker rows · 15,560 participants · PostgreSQL

The core architectural decision: a **registry pattern** where every biomarker and medical history variable maps to a human-readable name in a central registry table. NHANES column codes (`LBXGH`, `URXUMA`) never appear in analysis code. Adding a new biomarker means inserting one row. Running a new analysis means calling the same functions with different inputs.

### Evidence Generated

| Analysis | Cohort | Key Finding |
|---|---|---|
| Urine biomarkers vs obesity | Adults ≥ 18 (n=2,898) | Low predictive value (R²=0.053); creatinine significant, likely via muscle mass |
| Carbohydrate metabolism vs obesity | Adults ≥ 18, diabetics excluded (n=3,478) | Insulin strongest correlate (r=0.556); each 1% HbA1c → 2.26× obesity odds |
| SHBG vs obesity — males 22–49 | Males 22–49 (n=1,387) | Strong inverse relationship (r=−0.352); highest vs lowest SHBG quartile: 83% lower obesity odds |
| SHBG vs obesity — females 18–44 | Females 18–44, negative pregnancy test (n=1,308) | Consistent inverse relationship (r=−0.321); 82.9% lower obesity odds in highest SHBG quartile |
| Reproductive hormones by cycle phase | Females 18–44, phase-classified (n=1,308) | Estrone-SHBG relationship is phase-dependent — only emerges in luteal phase (β=0.255, p<0.001) |

The reproductive hormone analysis required data-driven menstrual cycle phase classification using a **Gaussian Mixture Model on log-transformed progesterone** — because NHANES doesn't capture cycle phase directly.

### Pipeline Flow

```
Raw XPT Files → PostgreSQL (raw schema)
      ↓
biomarker_registry + medhx_registry    ← auto-scraped from CDC codebooks
      ↓
participant_biomarkers (2M+ rows)
participant_medhx (1.5M+ rows)
participant_demographics (15,560 rows)
      ↓
nhanes_analysis.py                     ← 8 reusable analysis functions
      ↓
Cohort descriptives · Correlation · Linear regression · Logistic regression · Quartile analysis
```

### Methodological Standards

- Disease definitions from clinical guidelines (WHO, ACC/AHA 2017, ADA)
- Log transformation applied where skewness > 1; untransformed values retained for logistic regression to preserve interpretable odds ratios
- Covariates configurable per analysis; sex auto-excluded for single-sex cohorts
- Survey weights collected and stored for future population-level inference
- Cross-sectional design — all associations observational, causality not inferred

**→ [NHANES Pipeline](NHANES_analysis/pipeline/README.md)**

---

## Additional Projects

### Appointment No-Show Analysis
Exploratory analysis of a Kaggle appointment dataset examining patterns in patient no-shows.

**→ [Appointment Analysis](Appointment_analysis/)**

---

## Stack

Python · PostgreSQL · pandas · statsmodels · scikit-learn · SQLAlchemy · seaborn · BeautifulSoup · Jupyter
