"""
nhanes_analysis.py
------------------
Reusable analysis functions for NHANES pipeline.

All functions take:
- biomarkers : str or list of str  (biomarker_name from biomarker_registry)
- disease    : str                 (key from DISEASE_CONFIGS)
- engine     : SQLAlchemy engine   (PostgreSQL connection)

Usage:
    from nhanes_analysis import load_analysis_data, run_correlation, run_scatter
                                   run_regression, run_logistic_regression
    from disease_config import DISEASE_CONFIGS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
import statsmodels.api as sm
from disease_config import DISEASE_CONFIGS


# ── Covariates always included in regression models ────────────────────────────
COVARIATES = ["age", "sex", "race_ethnicity"]


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADER
# ═══════════════════════════════════════════════════════════════════════════════

def load_analysis_data(biomarkers, disease, engine):
    """
    Pulls and merges everything needed for an analysis from PostgreSQL.

    Parameters
    ----------
    biomarkers : str or list of str
        One or more biomarker_name values from biomarker_registry.
    disease    : str
        Key from DISEASE_CONFIGS (e.g. 'obesity', 'hypertension', 'diabetes').
    engine     : SQLAlchemy engine

    Returns
    -------
    df : DataFrame with columns:
         participant_id, <biomarker_name(s)>, <outcome_col(s)>,
         age, sex, race_ethnicity, <binary_col>
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]

    # ── 1. Pull biomarker values from long table ───────────────────────────────
    biomarker_placeholders = ", ".join([f"'{b}'" for b in biomarkers])

    bio_df = pd.read_sql(f"""
        SELECT pb.participant_id,
               br.biomarker_name,
               pb.value
        FROM participant_biomarkers pb
        JOIN biomarker_registry br USING (biomarker_id)
        WHERE br.biomarker_name IN ({biomarker_placeholders})
    """, engine)

    # Pivot long → wide so each biomarker is its own column
    bio_wide = bio_df.pivot_table(
        index="participant_id",
        columns="biomarker_name",
        values="value",
        aggfunc="mean"   # handles rare duplicates
    ).reset_index()
    bio_wide.columns.name = None

    # ── 2. Pull demographics + outcome columns ─────────────────────────────────
    # Determine which outcome columns to pull
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

    # ── 3. Special case: diabetes outcome (hba1c) lives in biomarkers ──────────
    # If the outcome is already in bio_wide, don't pull it again
    if disease == "diabetes" and "hba1c" in bio_wide.columns:
        outcome_col = config["outcome_col"]
        demo_df[outcome_col] = bio_wide.set_index("participant_id")["hba1c"]

    # ── 4. Merge biomarkers + demographics ────────────────────────────────────
    df = demo_df.merge(bio_wide, on="participant_id", how="inner")

    # ── 5. Create binary disease column ───────────────────────────────────────
    binary_col = config["binary_col"]

    if disease == "hypertension":
        df[binary_col] = (
            (df["systolic_bp"]  >= config["thresholds"]["systolic_bp"]["value"]) |
            (df["diastolic_bp"] >= config["thresholds"]["diastolic_bp"]["value"])
        ).astype(int)
    else:
        outcome = config["outcome_col"]
        threshold = config["threshold"]
        df[binary_col] = (df[outcome] >= threshold).astype(int)

    # ── 6. Drop rows missing any key column ───────────────────────────────────
    key_cols = biomarkers + COVARIATES + [binary_col]
    before = len(df)
    df = df.dropna(subset=key_cols).copy()
    print(f"Participants after dropping missing values: {len(df):,} ({before - len(df):,} dropped)")

    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CORRELATION
# ═══════════════════════════════════════════════════════════════════════════════

def run_correlation(biomarkers, disease, engine, method="spearman"):
    """
    Runs correlation between each biomarker and the continuous outcome.

    Parameters
    ----------
    biomarkers : str or list of str
    disease    : str
    engine     : SQLAlchemy engine
    method     : 'spearman' (default) or 'pearson'

    Returns
    -------
    results_df : DataFrame with biomarker, correlation, p_value, n
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]

    # Hypertension uses systolic as the primary continuous outcome
    if disease == "hypertension":
        outcome_col = "systolic_bp"
    else:
        outcome_col = config["outcome_col"]

    df = load_analysis_data(biomarkers, disease, engine)

    results = []
    for bio in biomarkers:
        if bio not in df.columns:
            print(f"⚠ {bio} not found in data, skipping")
            continue

        clean = df[[bio, outcome_col]].dropna()
        n = len(clean)

        if method == "spearman":
            corr, pval = stats.spearmanr(clean[bio], clean[outcome_col])
        else:
            corr, pval = stats.pearsonr(clean[bio], clean[outcome_col])

        results.append({
            "biomarker":   bio,
            "outcome":     outcome_col,
            "correlation": round(corr, 4),
            "p_value":     round(pval, 6),
            "n":           n,
            "method":      method,
            "significant": pval < 0.05
        })

    results_df = pd.DataFrame(results).sort_values("correlation", ascending=False)
    print(f"\n{method.capitalize()} Correlation — {config['label']}")
    print(results_df.to_string(index=False))
    return results_df


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SCATTER PLOT
# ═══════════════════════════════════════════════════════════════════════════════

def run_scatter(biomarker, disease, engine, hue_col="sex_label"):
    """
    Scatter plot of a single biomarker vs the continuous outcome.

    Parameters
    ----------
    biomarker : str
    disease   : str
    engine    : SQLAlchemy engine
    hue_col   : column to color points by (default 'sex_label')
    """
    config = DISEASE_CONFIGS[disease]

    if disease == "hypertension":
        outcome_col = "systolic_bp"
    else:
        outcome_col = config["outcome_col"]

    df = load_analysis_data(biomarker, disease, engine)

    # Pull sex_label separately if needed for hue
    if hue_col == "sex_label":
        sex_labels = pd.read_sql(
            "SELECT participant_id, sex_label FROM participant_demographics", engine
        )
        df = df.merge(sex_labels, on="participant_id", how="left")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x=biomarker,
        y=outcome_col,
        hue=hue_col if hue_col in df.columns else None,
        alpha=0.4,
        s=20,
        ax=ax
    )
    sns.regplot(
        data=df,
        x=biomarker,
        y=outcome_col,
        scatter=False,
        color="red",
        ax=ax
    )

    ax.set_title(f"{biomarker} vs {outcome_col} — {config['label']}", fontsize=13)
    ax.set_xlabel(biomarker)
    ax.set_ylabel(outcome_col)
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# 4. LINEAR REGRESSION (continuous outcome)
# ═══════════════════════════════════════════════════════════════════════════════

def run_linear_regression(biomarkers, disease, engine):
    """
    Linear regression: outcome ~ biomarker(s) + age + sex + race_ethnicity.
    Works for single or multiple biomarkers (multivariate).

    Parameters
    ----------
    biomarkers : str or list of str
    disease    : str
    engine     : SQLAlchemy engine

    Returns
    -------
    Statsmodels OLS results summary
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]

    if disease == "hypertension":
        outcome_col = "systolic_bp"
    else:
        outcome_col = config["outcome_col"]

    df = load_analysis_data(biomarkers, disease, engine)

    # Build formula string
    predictors = biomarkers + COVARIATES
    formula = f"{outcome_col} ~ " + " + ".join(predictors)
    print(f"\nFormula: {formula}")

    model = smf.ols(formula=formula, data=df).fit()
    print(model.summary())
    return model


# ═══════════════════════════════════════════════════════════════════════════════
# 5. LOGISTIC REGRESSION (binary outcome)
# ═══════════════════════════════════════════════════════════════════════════════

def run_logistic_regression(biomarkers, disease, engine):
    """
    Logistic regression: binary_outcome ~ biomarker(s) + age + sex + race_ethnicity.
    Works for single or multiple biomarkers (multivariate).
    Reports odds ratios and 95% confidence intervals.

    Parameters
    ----------
    biomarkers : str or list of str
    disease    : str
    engine     : SQLAlchemy engine

    Returns
    -------
    odds_df    : DataFrame with odds ratios, CIs, and p-values
    model      : Statsmodels logit model
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config  = DISEASE_CONFIGS[disease]
    bin_col = config["binary_col"]

    df = load_analysis_data(biomarkers, disease, engine)

    # Build formula
    predictors = biomarkers + COVARIATES
    formula = f"{bin_col} ~ " + " + ".join(predictors)
    print(f"\nFormula: {formula}")

    model = smf.logit(formula=formula, data=df).fit(disp=False)

    # Extract odds ratios + 95% CI
    odds_df = pd.DataFrame({
        "odds_ratio":  np.exp(model.params),
        "ci_lower":    np.exp(model.conf_int()[0]),
        "ci_upper":    np.exp(model.conf_int()[1]),
        "p_value":     model.pvalues
    }).round(4)

    odds_df["significant"] = odds_df["p_value"] < 0.05
    print(f"\nLogistic Regression — {config['label']}")
    print(odds_df.to_string())

    return odds_df, model
