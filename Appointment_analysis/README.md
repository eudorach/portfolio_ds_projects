# Medical Appointment No-Show Analysis (Kaggle Dataset)
---

## Why This Project Exists

Missed outpatient appointments are more than scheduling inconveniences — they represent operational inefficiency, delayed care, disrupted continuity, and lost clinical capacity. In high-volume healthcare systems, even modest no-show rates can create downstream effects on staffing, access to care, and revenue cycle performance.

Having worked in clinical environments where missed appointments directly affected workflow and patient follow-up, I wanted to explore a practical question:

Which patient characteristics meaningfully associate with appointment no-show behavior, and are those patterns primarily demographic, clinical, or both?

This project analyzes outpatient appointment attendance patterns using structured SQL-based cohort analysis and exploratory stratification techniques.

---

## What I Found (Short Version)
**1. Appointment lead time is the strongest driver of no-shows**

No-show rates increase substantially as the time between scheduling and appointment date increases. Same-day appointments show very low no-show rates (~2–7%), while appointments scheduled 30+ days in advance show significantly higher no-show rates (~20–40%). This pattern is consistent across all age groups.

**2. Age modifies baseline risk but does not override scheduling effects**

Younger patients (18–35) consistently exhibit higher no-show rates across all wait-time categories. Older patients (65+) show lower baseline risk but remain sensitive to long scheduling delays. This indicates that age acts as a risk modifier rather than a primary driver.

**3. Highest-risk combinations occur at the intersection of age and wait time**

Stratified analysis shows that the highest no-show rates occur among younger patients with long appointment lead times. Conversely, older patients with short lead times consistently exhibit the lowest no-show rates.

**4. SMS reminders are associated with higher observed no-show rates due to selection bias**

Across all age groups and wait-time strata, patients receiving SMS reminders exhibit higher no-show rates than those who do not. This pattern is consistent with non-random assignment of SMS reminders to higher-risk patients rather than a causal effect of SMS increasing no-shows.

Within comparable wait-time and age strata, SMS effects vary but do not show consistent evidence of uniformly reducing no-show behavior.

**5. Interaction effects provide more insight than single-variable analysis**

Multivariate stratification (age × wait time × SMS) reveals that no-show behavior is structured by overlapping risk factors rather than isolated predictors. Operational variables (wait time) dominate, while demographic and intervention variables modulate baseline risk.

**6. Chronic conditions show limited explanatory power**

Chronic conditions such as diabetes, hypertension, and alcoholism showed weak and inconsistent associations with no-show behavior when analyzed alongside age and scheduling variables. These factors did not meaningfully stratify no-show risk compared to operational (wait time) and demographic (age) variables.

This suggests that clinical comorbidity alone is not a strong predictor of missed appointments in this dataset when compared to structural scheduling factors.

---

## Dataset

Public outpatient appointment dataset containing patient scheduling and attendance records, including:

- Patient demographics (age, gender)
- Chronic disease indicators (diabetes, hypertension, alcoholism)
- Appointment attendance outcome (show vs. no-show)
- SMS reminder status
- Attendance outcome (show vs. no-show)

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
- Computation of appointment lead time (scheduled vs appointment date)
- Binary encoding of no-show outcomes
- Standardization of categorical variables

### Exploratory Cohort Analysis

Analyses included:

- Age-stratified no-show rates
- Wait-time bucket analysis
- SMS reminder comparisons
- Multi-variable interaction exploration (age × wait time × SMS)

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

No-show behavior is primarily driven by operational scheduling structure rather than patient-level clinical conditions alone.

Key implications include:

- Scheduling lead time is a critical operational lever for reducing no-shows
- Demographic factors modify risk but do not dominate it
- Reminder systems (SMS) are likely applied non-randomly and require careful interpretation
- Intervention design should account for underlying risk stratification rather than assume uniform treatment effects

This type of exploratory analysis reflects early-stage healthcare operations analytics, where cohort-level insights guide intervention and optimization strategies.

---

## Reproducibility

All analyses were performed using reproducible SQL workflows with cohort logic documented directly within query structures.

This project is ongoing. Future analyses will expand into multivariable modeling and additional operational attendance patterns.
