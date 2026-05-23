"""
nhanes_analysis.py
------------------
Reusable analysis functions for NHANES pipeline.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.formula.api as smf
from diagnosis_config import DISEASE_CONFIGS

COVARIATES = ["age", "sex", "race_ethnicity"]


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_analysis_data(biomarkers, disease, engine, filters=None):
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    filters = filters or {}
    config  = DISEASE_CONFIGS[disease]

    # ── 1. Pull biomarker values ───────────────────────────────────────────────
    biomarker_placeholders = ", ".join([f"'{b}'" for b in biomarkers])
    bio_df = pd.read_sql(f"""
        SELECT pb.participant_id,
               br.biomarker_name,
               pb.value
        FROM participant_biomarkers pb
        JOIN biomarker_registry br USING (biomarker_id)
        WHERE br.biomarker_name IN ({biomarker_placeholders})
    """, engine)

    bio_wide = bio_df.pivot_table(
        index="participant_id",
        columns="biomarker_name",
        values="value",
        aggfunc="mean"
    ).reset_index()
    bio_wide.columns.name = None

    # ── 2. Pull demographics + outcome columns ─────────────────────────────────
    if disease == "hypertension":
        outcome_cols = "systolic_bp, diastolic_bp"
    else:
        outcome_cols = config["outcome_col"]

    demo_df = pd.read_sql(f"""
        SELECT participant_id,
               {outcome_cols},
               age, sex, race_ethnicity
        FROM participant_demographics
    """, engine)

    # ── 3. Merge ───────────────────────────────────────────────────────────────
    df = demo_df.merge(bio_wide, on="participant_id", how="inner")

    # ── 4. Apply age filter ────────────────────────────────────────────────────
    min_age = filters.get("min_age", 18)
    df = df[df["age"] >= min_age].copy()
    print(f"After age filter (>= {min_age}): {len(df):,} participants")

    # ── 5. Exclude diabetes if requested ──────────────────────────────────────
    if filters.get("exclude_diabetes", False):
        before   = len(df)
        criteria = filters.get("diabetes_criteria", "both")

        exclusion_df = pd.read_sql("""
            SELECT pb.participant_id,
                   br.biomarker_name,
                   pb.value
            FROM participant_biomarkers pb
            JOIN biomarker_registry br USING (biomarker_id)
            WHERE br.biomarker_name IN ('glycohemoglobin', 'fasting_glucose')
        """, engine)

        excl_wide = exclusion_df.pivot_table(
            index="participant_id",
            columns="biomarker_name",
            values="value",
            aggfunc="mean"
        ).reset_index()
        excl_wide.columns.name = None

        # Only merge columns we don't already have in df
        cols_to_add = [col for col in ["glycohemoglobin", "fasting_glucose"]
                       if col not in df.columns]
        if cols_to_add:
            excl_subset = excl_wide[["participant_id"] + cols_to_add]
            df = df.merge(excl_subset, on="participant_id", how="left")

        # Drop rows where we can't confirm non-diabetic status
        if criteria == "hba1c_only":
            df = df.dropna(subset=["glycohemoglobin"]).copy()
        else:
            df = df.dropna(subset=["glycohemoglobin", "fasting_glucose"]).copy()

        # Exclude confirmed diabetics
        if criteria == "hba1c_only":
            diabetic_mask = (df["glycohemoglobin"] >= 6.5)
        elif criteria == "glucose_only":
            diabetic_mask = (df["fasting_glucose"] >= 126)
        else:
            diabetic_mask = (
                (df["glycohemoglobin"] >= 6.5) |
                (df["fasting_glucose"] >= 126)
            )
        df = df[~diabetic_mask].copy()

        # Drop exclusion columns if not in original biomarker list
        for col in ["glycohemoglobin", "fasting_glucose"]:
            if col not in biomarkers and col in df.columns:
                df = df.drop(columns=[col])

        print(f"After excluding diabetes: {len(df):,} ({before - len(df):,} excluded)")

    # ── 6. Create binary disease column ───────────────────────────────────────
    binary_col = config["binary_col"]

    if disease == "hypertension":
        df[binary_col] = (
            (df["systolic_bp"]  >= config["thresholds"]["systolic_bp"]["value"]) |
            (df["diastolic_bp"] >= config["thresholds"]["diastolic_bp"]["value"])
        ).astype(int)
    else:
        outcome   = config["outcome_col"]
        threshold = config["threshold"]
        df[binary_col] = (df[outcome] >= threshold).astype(int)

    # ── 7. Drop rows missing any key column ───────────────────────────────────
    key_cols = biomarkers + COVARIATES + [binary_col]
    before   = len(df)
    df = df.dropna(subset=key_cols).copy()
    print(f"After dropping missing values: {len(df):,} ({before - len(df):,} dropped)")

    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CORRELATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_correlation(biomarkers, disease, engine, method="spearman", log_transform=False, filters=None):
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]
    outcome_col = "systolic_bp" if disease == "hypertension" else config["outcome_col"]

    df = load_analysis_data(biomarkers, disease, engine, filters=filters)

    results = []
    for bio in biomarkers:
        clean = df[[bio, outcome_col]].dropna()
        if log_transform:
            clean = clean[clean[bio] > 0]
            clean[bio] = np.log(clean[bio])
        n = len(clean)
        if method == "spearman":
            corr, pval = stats.spearmanr(clean[bio], clean[outcome_col])
        else:
            corr, pval = stats.pearsonr(clean[bio], clean[outcome_col])
        results.append({
            "biomarker":     bio,
            "outcome":       outcome_col,
            "correlation":   round(corr, 4),
            "p_value":       round(pval, 6),
            "n":             n,
            "log_transform": log_transform,
            "method":        method,
            "significant":   pval < 0.05
        })

    results_df = pd.DataFrame(results).sort_values("correlation", ascending=False)
    print(f"\n{method.capitalize()} Correlation — {config['label']}")
    print(results_df.to_string(index=False))
    return results_df


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SCATTER PLOT
# ═══════════════════════════════════════════════════════════════════════════════

def run_scatter(biomarker, disease, engine, hue_col="sex_label", filters=None):
    config      = DISEASE_CONFIGS[disease]
    outcome_col = "systolic_bp" if disease == "hypertension" else config["outcome_col"]

    df = load_analysis_data(biomarker, disease, engine, filters=filters)

    if hue_col == "sex_label":
        sex_labels = pd.read_sql(
            "SELECT participant_id, sex_label FROM participant_demographics", engine
        )
        df = df.merge(sex_labels, on="participant_id", how="left")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x=biomarker, y=outcome_col,
                    hue=hue_col if hue_col in df.columns else None,
                    alpha=0.4, s=20, ax=ax)
    sns.regplot(data=df, x=biomarker, y=outcome_col,
                scatter=False, color="red", ax=ax)
    ax.set_title(f"{biomarker} vs {outcome_col} — {config['label']}", fontsize=13)
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. LINEAR REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

def run_linear_regression(biomarkers, disease, engine, log_transform=False, filters=None):
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config      = DISEASE_CONFIGS[disease]
    outcome_col = "systolic_bp" if disease == "hypertension" else config["outcome_col"]

    df = load_analysis_data(biomarkers, disease, engine, filters=filters)

    if log_transform:
        for bio in biomarkers:
            df = df[df[bio] > 0]
            df[bio] = np.log(df[bio])

    predictors = biomarkers + COVARIATES
    formula    = f"{outcome_col} ~ " + " + ".join(predictors)
    print(f"\nFormula: {formula}")

    model = smf.ols(formula=formula, data=df).fit()
    print(model.summary())
    return model


# ═══════════════════════════════════════════════════════════════════════════════
# 5. LOGISTIC REGRESSION
# ═══════════════════════════════════════════════════════════════════════════════

def run_logistic_regression(biomarkers, disease, engine, log_transform=False, filters=None):
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config  = DISEASE_CONFIGS[disease]
    bin_col = config["binary_col"]

    df = load_analysis_data(biomarkers, disease, engine, filters=filters)

    if log_transform:
        for bio in biomarkers:
            df = df[df[bio] > 0]
            df[bio] = np.log(df[bio])

    predictors = biomarkers + COVARIATES
    formula    = f"{bin_col} ~ " + " + ".join(predictors)
    print(f"\nFormula: {formula}")

    model  = smf.logit(formula=formula, data=df).fit(disp=False)
    odds_df = pd.DataFrame({
        "odds_ratio": np.exp(model.params),
        "ci_lower":   np.exp(model.conf_int()[0]),
        "ci_upper":   np.exp(model.conf_int()[1]),
        "p_value":    model.pvalues
    }).round(4)
    odds_df["significant"] = odds_df["p_value"] < 0.05

    print(f"\nLogistic Regression — {config['label']}")
    print(odds_df.to_string())
    return odds_df, model