# NHANES Obesity and Biomarkers Study

## Overview
This project uses NHANES 2017–2020 datasets to explore relationships between biomarkers (primarily from blood and urine lab results) and obesity. The final goal is to clean and organize this data into a relational database for predictive modeling and analysis.

## Objective
The goal of this project is to explore the relationships between clinical lab measurements and metabolic health, particularly focusing on obesity. By analyzing urine and blood lab values, the project aims to identify potential biomarkers associated with metabolic conditions. This includes assessing kidney function, thyroid function, and other metabolic indicators to better understand how these biological parameters relate to body mass index (BMI) and overall metabolic status.

The analysis is structured to be reproducible and modular, with cleaned datasets stored in a relational database, enabling both descriptive and predictive analyses.

### Urine Lab Analysis
With the cleaned and individually exported data, the dataset is now ready for detailed analysis. The urine lab data will be analyzed first, followed by blood lab analyses.

From the cleaned urine labs, the focus will be on values that are more directly associated with metabolic syndrome and related conditions. The urine labs selected for analysis are:

* Albumin – Used to assess kidney function and nutritional status.
* Creatinine – Another key marker of kidney function.
* Iodine – An essential element for thyroid function, which plays a direct role in metabolism.

These analytes were chosen for their relevance to metabolic health and potential associations with obesity and related physiological outcomes.

### Blood Lab Analysis
---

## Data Sources
- NHANES 2017–2020: [https://wwwn.cdc.gov/nchs/nhanes/](https://wwwn.cdc.gov/nchs/nhanes/)

## Data Cleaning
The NHANES data consists of multiple datasets grouped into distinct categories. For this project, I categorized them into:

- Demographics
- Body Measurements
- Urine Lab Values
- Blood Lab Values

To improve efficiency and ensure reproducibility, I cleaned each category in a separate Jupyter notebook. This modular approach also improves readability and makes it easier to track preprocessing steps for each dataset type.

### Functions

#### `drop_rows_with_both_nans()`
Removes rows where both `col1` and `col2` are NaN.

#### `get_common_nan_ids()`
Identifies participant IDs with NaNs in both columns. Useful for understanding overlap in missing data.

#### `standardize_id_column()`
Renames the original identifier column to 'participant_id'
...

### Column Changes
- Renamed columns are tracked in the [Variable Key](#variable-key-column-renaming)
- Encoded values are kept in raw format; meanings are described above.

## Merging Datasets

All datasets are merged using `participant_id` as the key. Merges are typically done using an inner join to preserve only complete records.

```python
merged_df = df1.merge(df2, on='participant_id', how='inner')
