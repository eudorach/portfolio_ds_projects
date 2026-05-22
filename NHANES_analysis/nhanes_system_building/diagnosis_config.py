"""
disease_config.py
-----------------
Defines disease states for NHANES analysis.

Each disease has:
- outcome_col    : column in participant_demographics to use
- continuous     : use outcome as a continuous number
- binary_col     : name for the 0/1 case/control column
- threshold      : cutoff to define a "case"
- threshold_dir  : "gte" (>=) or "lte" (<=)
- label          : human readable name
- notes          : clinical definition reference
"""

DISEASE_CONFIGS = {

    "obesity": {
        "outcome_col":    "bmi",
        "continuous":     True,
        "binary_col":     "obese",
        "threshold":      30,
        "threshold_dir":  "gte",
        "label":          "Obesity",
        "notes":          "WHO definition: BMI >= 30 kg/m²"
    },

    "hypertension": {
    "outcome_cols": {
        "systolic":  "systolic_bp",
        "diastolic": "diastolic_bp"
    },
    "continuous":     True,
    "binary_col":     "hypertensive",
    "thresholds": {
        "systolic_bp":  {"value": 130, "dir": "gte"},
        "diastolic_bp": {"value": 80,  "dir": "gte"}
    },
    "threshold_logic": "either",   # case if systolic OR diastolic meets threshold
    "label":          "Hypertension",
    "notes":          "ACC/AHA 2017: systolic BP >= 130 mmHg OR diastolic BP >= 80 mmHg"
    },

    "diabetes": {
        "outcome_col":    "hba1c",
        "continuous":     True,
        "binary_col":     "diabetic",
        "threshold":      6.5,
        "threshold_dir":  "gte",
        "label":          "Diabetes",
        "notes":          "ADA definition: HbA1c >= 6.5%"
    },

}