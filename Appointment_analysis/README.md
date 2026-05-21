# Medical Appointment No-Show Analysis (Kaggle Dataset)--In Progress
---

## Why This Project Exists

Missed outpatient appointments are more than scheduling inconveniences — they represent operational inefficiency, delayed care, disrupted continuity, and lost clinical capacity. In high-volume healthcare systems, even modest no-show rates can create downstream effects on staffing, access to care, and revenue cycle performance.

Having worked in clinical environments where missed appointments directly affected workflow and patient follow-up, I wanted to explore a practical question:

Which patient characteristics meaningfully associate with appointment no-show behavior, and are those patterns primarily demographic, clinical, or both?

This project analyzes outpatient appointment attendance patterns using structured SQL-based cohort analysis and exploratory stratification techniques.

---

## What I Found (Short Version)
**Demographic factors showed stronger associations with no-show behavior than chronic disease status.**

Younger adult cohorts consistently demonstrated higher no-show rates compared to older adults, suggesting that age-related behavioral or socioeconomic factors may play a larger role than medical comorbidity burden alone.

**Gender differences were modest but persistent across stratified cohorts.**

Female patients represented a larger proportion of appointments overall, while subgroup analyses showed small but observable differences in attendance behavior across demographic strata.

**Chronic conditions alone added limited explanatory value.**

Diabetes, hypertension, and alcoholism showed weaker independent associations with no-show behavior than expected when analyzed alongside age and gender cohorts.

**Interaction effects provided more insight than single-variable analysis.**

Stratified cohort analysis suggested that combinations of demographic and behavioral variables may be more informative than isolated predictors alone, highlighting the importance of multivariable modeling in operational healthcare analytics.

**Exploratory SQL analysis revealed the limitations of simple descriptive approaches.**

Early aggregation queries identified broad attendance patterns, but subgroup interactions and overlapping demographic effects demonstrated why healthcare operational problems often require layered analytical approaches rather than single-factor explanations.

---

## Dataset

Public outpatient appointment dataset containing patient scheduling and attendance records, including:

- Patient demographics (age, gender)
- Chronic disease indicators (diabetes, hypertension, alcoholism)
- Appointment attendance outcome (show vs. no-show)

Source: [Kaggle Medical Appointment No-Show dataset](https://www.kaggle.com/datasets/iamtanmayshukla/healthcare-no-shows-appointments-dataset)

---

## Technical Approach

### Data Architecture

The project was developed using DuckDB with SQL-first exploratory workflows designed to mimic lightweight analytical querying environments commonly used in healthcare operations and reporting pipelines.

The workflow emphasized:

- Reproducible cohort generation
- SQL-based feature engineering
- Stratified aggregation analysis
- Operationally interpretable subgroup comparisons

---

## Data Processing Pipeline

### Feature Engineering

Key preprocessing steps included:

- Creation of age-group cohorts
- Binary encoding of no-show outcomes
- Standardization of categorical variables
- Cohort stratification across demographic and clinical variables

### Exploratory Cohort Analysis

Analyses included:

- Age-stratified no-show rates
- Gender subgroup comparisons
- Chronic disease subgroup analysis
- Multi-variable interaction exploration

---

## 🧾 Example SQL Approach

```sql
WITH base AS (
    SELECT *,
        CASE 
            WHEN age < 18 THEN 'pediatric'
            WHEN age BETWEEN 18 AND 25 THEN '18-25'
            WHEN age BETWEEN 26 AND 35 THEN '26-35'
            WHEN age BETWEEN 36 AND 45 THEN '36-45'
            WHEN age BETWEEN 46 AND 55 THEN '46-55'
            WHEN age BETWEEN 56 AND 65 THEN '56-65'
            WHEN age BETWEEN 66 AND 75 THEN '66-75'
            ELSE 'senior'
        END AS age_group,

        CASE WHEN Showed_up = FALSE THEN 1 ELSE 0 END AS no_show_flag
    FROM appointments
)

SELECT 
    age_group,
    gender,
    diabetes,
    alcoholism,
    AVG(no_show_flag) AS no_show_rate,
    COUNT(*) AS total_appointments
FROM base
```
---

## Analytical Methods
- SQL cohort aggregation
- Stratified subgroup analysis
- Binary outcome analysis
- Exploratory interaction analysis
- Descriptive operational analytics

Tools:

- DuckDB
- SQL
- Python
- pandas

---

## Real-World Operational Implications

No-show prediction is fundamentally an operational healthcare problem. Identifying which patient populations are at higher risk for missed appointments can inform:

- Scheduling optimization strategies
- Reminder and outreach interventions
- Resource allocation
- Staffing efficiency
- Access-to-care initiatives

This type of exploratory analysis mirrors the early stages of healthcare operations analytics, where simple cohort-level patterns often guide subsequent predictive modeling and intervention design.

---

## Reproducibility

All analyses were performed using reproducible SQL workflows with cohort logic documented directly within query structures.

This project is ongoing. Future analyses will expand into multivariable modeling and additional operational attendance patterns.
