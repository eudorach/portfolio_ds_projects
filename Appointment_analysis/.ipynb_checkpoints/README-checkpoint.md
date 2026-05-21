# Medical Appointment No-Show Analysis (Kaggle Dataset)

## 📌 Overview
This project explores factors associated with patient no-show behavior in outpatient medical appointments. The goal is to identify whether demographic characteristics (age, gender) and clinical conditions (diabetes, alcoholism) are associated with missed appointments.

The analysis was performed using SQL (DuckDB) with cohort-based stratification and iterative exploratory analysis.

---

## 📊 Dataset
The dataset contains outpatient appointment records, including:

- Patient demographics (age, gender)
- Health conditions (diabetes, hypertension, alcoholism)
- Appointment attendance status (show / no-show)

Source: Kaggle Medical Appointment No-Show dataset

---

## 🧪 Methodology

The analysis was conducted using a structured exploratory approach:

1. Data cleaning and feature engineering
   - Created age group bins
   - Converted outcome variable into binary no-show flag

2. Cohort-based aggregation using SQL
   - Stratified by age group, gender, and clinical conditions
   - Calculated no-show rates using average of binary indicator

3. Interaction analysis
   - Examined combined effects of age, gender, and alcoholism
   - Evaluated whether clinical conditions add explanatory power beyond demographics

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
GROUP BY age_group, gender, diabetes, alcoholism;
