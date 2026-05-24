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
    min_age = filters.get("min_age", None)
    max_age = filters.get("max_age", None)
    age_range = filters.get("age_range", None)  # tuple e.g. (30, 60)

    if age_range:
        df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])].copy()
        print(f"After age filter ({age_range[0]}–{age_range[1]}): {len(df):,} participants")
    elif min_age and max_age:
        df = df[(df["age"] >= min_age) & (df["age"] <= max_age)].copy()
        print(f"After age filter ({min_age}–{max_age}): {len(df):,} participants")
    elif min_age:
        df = df[df["age"] >= min_age].copy()
        print(f"After age filter (>= {min_age}): {len(df):,} participants")
    elif max_age:
        df = df[df["age"] <= max_age].copy()
        print(f"After age filter (<= {max_age}): {len(df):,} participants")
    
    # ── 4b. Apply sex filter ───────────────────────────────────────────────────
    sex_filter = filters.get("sex", None)  # 1 = Male, 2 = Female

    if sex_filter:
        before = len(df)
        df = df[df["sex"] == sex_filter].copy()
        sex_label = "Males" if sex_filter == 1 else "Females"
        print(f"After sex filter ({sex_label}): {len(df):,} participants ({before - len(df):,} excluded)")
        
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
# 2. COHORT DESCRIPTIVES
# ═══════════════════════════════════════════════════════════════════════════════

def run_cohort_descriptives(biomarkers, disease, engine, filters=None):
    """
    Descriptive statistics for the filtered cohort.
    - Categorical: sex, race/ethnicity — counts and percentages
    - Continuous: age, BMI, systolic BP, diastolic BP — mean, median, SD, min, max, IQR

    Parameters
    ----------
    biomarkers : str or list — needed to apply the same filters as your analysis
    disease    : str
    engine     : SQLAlchemy engine
    filters    : dict, optional

    Returns
    -------
    Prints formatted tables. Returns (continuous_df, categorical_df)
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]

    # Load full demographics for the filtered cohort
    demo_df = pd.read_sql("""
        SELECT participant_id, age, sex, sex_label,
               race_ethnicity, race_ethnicity_label,
               bmi, systolic_bp, diastolic_bp
        FROM participant_demographics
    """, engine)

    # Get filtered participant IDs by running load_analysis_data
    df = load_analysis_data(biomarkers, disease, engine, filters=filters)
    filtered_ids = df["participant_id"]

    # Filter demographics to matched cohort
    cohort = demo_df[demo_df["participant_id"].isin(filtered_ids)].copy()

    print(f"\n{'='*55}")
    print(f"Cohort Description — {config['label']} (n = {len(cohort):,})")
    print(f"{'='*55}")

    # ── Continuous variables ───────────────────────────────────────────────────
    continuous_cols = {
        "age":          "Age (years)",
        "bmi":          "BMI (kg/m²)",
        "systolic_bp":  "Systolic BP (mmHg)",
        "diastolic_bp": "Diastolic BP (mmHg)"
    }

    cont_rows = []
    for col, label in continuous_cols.items():
        if col in cohort.columns:
            vals = cohort[col].dropna()
            cont_rows.append({
                "Variable": label,
                "n":        len(vals),
                "Mean":     round(vals.mean(), 2),
                "SD":       round(vals.std(), 2),
                "Median":   round(vals.median(), 2),
                "IQR":      f"{round(vals.quantile(0.25), 1)}–{round(vals.quantile(0.75), 1)}",
                "Min":      round(vals.min(), 2),
                "Max":      round(vals.max(), 2),
            })

    cont_df = pd.DataFrame(cont_rows).set_index("Variable")
    print("\n── Continuous Variables ──────────────────────────────")
    print(cont_df.to_string())

    # ── Categorical variables ──────────────────────────────────────────────────
    print("\n── Sex ───────────────────────────────────────────────")
    sex_counts = cohort["sex_label"].value_counts()
    sex_pct    = (sex_counts / len(cohort) * 100).round(1)
    sex_df     = pd.DataFrame({"n": sex_counts, "%": sex_pct})
    print(sex_df.to_string())

    print("\n── Race/Ethnicity ────────────────────────────────────")
    race_counts = cohort["race_ethnicity_label"].value_counts()
    race_pct    = (race_counts / len(cohort) * 100).round(1)
    race_df     = pd.DataFrame({"n": race_counts, "%": race_pct})
    print(race_df.to_string())

    return cont_df, sex_df, race_df


# ═══════════════════════════════════════════════════════════════════════════════
# 3. BIOMARKER DESCRIPTIVES
# ═══════════════════════════════════════════════════════════════════════════════

def run_biomarker_descriptives(biomarkers, disease, engine, filters=None):
    """
    Descriptive statistics for each biomarker in the filtered cohort.
    Flags skewness > 1 as a recommendation to consider log transformation.

    Parameters
    ----------
    biomarkers : str or list of str
    disease    : str
    engine     : SQLAlchemy engine
    filters    : dict, optional

    Returns
    -------
    results_df : DataFrame with descriptive stats per biomarker
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]
    df     = load_analysis_data(biomarkers, disease, engine, filters=filters)

    # Pull units from registry for display
    placeholders = ", ".join([f"'{b}'" for b in biomarkers])
    units_df = pd.read_sql(f"""
        SELECT biomarker_name, unit
        FROM biomarker_registry
        WHERE biomarker_name IN ({placeholders})
    """, engine)
    units = dict(zip(units_df["biomarker_name"], units_df["unit"]))

    print(f"\n{'='*55}")
    print(f"Biomarker Descriptives — {config['label']}")
    print(f"{'='*55}")

    rows = []
    for bio in biomarkers:
        if bio not in df.columns:
            continue
        vals     = df[bio].dropna()
        skewness = round(vals.skew(), 3)
        rows.append({
            "Biomarker":  bio,
            "Unit":       units.get(bio, ""),
            "n":          len(vals),
            "Mean":       round(vals.mean(), 3),
            "SD":         round(vals.std(), 3),
            "Median":     round(vals.median(), 3),
            "IQR":        f"{round(vals.quantile(0.25), 2)}–{round(vals.quantile(0.75), 2)}",
            "Min":        round(vals.min(), 3),
            "Max":        round(vals.max(), 3),
            "Skewness":   skewness,
            "Kurtosis":   round(vals.kurtosis(), 3),
            "Log transform?": "Yes ✓" if abs(skewness) > 1 else "No"
        })

    results_df = pd.DataFrame(rows).set_index("Biomarker")
    print(results_df.to_string())
    print("\nNote: Log transform recommended when |Skewness| > 1")

    return results_df


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DISTRIBUTION PLOTS
# ═══════════════════════════════════════════════════════════════════════════════

def run_distribution_plots(biomarkers, disease, engine, filters=None):
    """
    Plots raw and log-transformed distributions for each biomarker.
    - ≤ 3 biomarkers → one row per biomarker, raw and log side by side
    - > 3 biomarkers → auto grid layout

    Parameters
    ----------
    biomarkers : str or list of str
    disease    : str
    engine     : SQLAlchemy engine
    filters    : dict, optional
    """
    if isinstance(biomarkers, str):
        biomarkers = [biomarkers]

    config = DISEASE_CONFIGS[disease]
    df     = load_analysis_data(biomarkers, disease, engine, filters=filters)

    n_bio  = len(biomarkers)

    if n_bio <= 3:
        # One row per biomarker, raw | log side by side
        fig, axes = plt.subplots(n_bio, 2, figsize=(12, 4 * n_bio))
        if n_bio == 1:
            axes = [axes]  # ensure iterable

        for i, bio in enumerate(biomarkers):
            vals = df[bio].dropna()
            skew_raw = round(vals.skew(), 3)

            # Raw distribution
            sns.histplot(vals, kde=True, ax=axes[i][0], color="steelblue")
            axes[i][0].set_title(f"{bio} — Raw\nSkewness: {skew_raw}", fontsize=11)
            axes[i][0].set_xlabel(bio)

            # Log distribution
            log_vals  = np.log(vals[vals > 0])
            skew_log  = round(log_vals.skew(), 3)
            sns.histplot(log_vals, kde=True, ax=axes[i][1], color="coral")
            axes[i][1].set_title(f"{bio} — Log Transformed\nSkewness: {skew_log}", fontsize=11)
            axes[i][1].set_xlabel(f"log({bio})")

    else:
        # Grid layout for > 3 biomarkers
        n_cols = 4  # raw + log for 2 biomarkers per row
        n_rows = int(np.ceil(n_bio / 2))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
        axes = axes.flatten()

        for i, bio in enumerate(biomarkers):
            vals     = df[bio].dropna()
            skew_raw = round(vals.skew(), 3)
            ax_raw   = axes[i * 2]
            ax_log   = axes[i * 2 + 1]

            sns.histplot(vals, kde=True, ax=ax_raw, color="steelblue")
            ax_raw.set_title(f"{bio}\nRaw | Skew: {skew_raw}", fontsize=10)

            log_vals = np.log(vals[vals > 0])
            skew_log = round(log_vals.skew(), 3)
            sns.histplot(log_vals, kde=True, ax=ax_log, color="coral")
            ax_log.set_title(f"{bio}\nLog | Skew: {skew_log}", fontsize=10)

        # Hide unused axes
        for j in range(n_bio * 2, len(axes)):
            axes[j].set_visible(False)

    fig.suptitle(f"Biomarker Distributions — {config['label']}", fontsize=13, y=1.01)
    plt.tight_layout()
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. CORRELATION
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
# 6. SCATTER PLOT
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
# 7. LINEAR REGRESSION
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
    
    # Remove sex from covariates if sex filter is applied
    covariates = COVARIATES.copy()
    if filters and filters.get("sex"):
        covariates.remove("sex")

    predictors = biomarkers + covariates
    formula    = f"{outcome_col} ~ " + " + ".join(predictors)
    print(f"\nFormula: {formula}")

    model = smf.ols(formula=formula, data=df).fit()
    print(model.summary())
    return model


# ═══════════════════════════════════════════════════════════════════════════════
# 8. LOGISTIC REGRESSION
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
    # ← add this temporarily
    print("biomarkers:", biomarkers)
    print("sample insulin values after log:", df["insulin"].head().tolist())
    print("sample glycohemoglobin values after log:", df["glycohemoglobin"].head().tolist())
            
    # Remove sex from covariates if sex filter is applied
    covariates = COVARIATES.copy()
    if filters and filters.get("sex"):
        covariates.remove("sex")

    predictors = biomarkers + covariates
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

# ═══════════════════════════════════════════════════════════════════════════════
# 9. QUARTILE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
 
def run_quartile_analysis(biomarker, disease, engine, log_transform=False, filters=None):
    """
    Quartile analysis for a single biomarker vs outcome.
 
    For each quartile (Q1 = reference):
    - Mean outcome (e.g. BMI) per quartile → bar chart
    - Logistic regression ORs with Q1 as reference → forest plot
    - Spearman correlation per quartile → trend table
 
    Parameters
    ----------
    biomarker    : str — single biomarker name
    disease      : str
    engine       : SQLAlchemy engine
    log_transform: bool — log transform before quartile assignment
    filters      : dict, optional
 
    Returns
    -------
    quartile_df  : DataFrame with per-quartile summary stats and ORs
    """
    if isinstance(biomarker, list):
        if len(biomarker) > 1:
            print("⚠ run_quartile_analysis() accepts one biomarker at a time. Using first.")
        biomarker = biomarker[0]
 
    config      = DISEASE_CONFIGS[disease]
    outcome_col = "systolic_bp" if disease == "hypertension" else config["outcome_col"]
    binary_col  = config["binary_col"]
 
    df = load_analysis_data(biomarker, disease, engine, filters=filters)
 
    # ── 1. Optional log transform ──────────────────────────────────────────────
    if log_transform:
        df = df[df[biomarker] > 0].copy()
        df[biomarker] = np.log(df[biomarker])
 
    # ── 2. Assign quartiles ────────────────────────────────────────────────────
    df["quartile"] = pd.qcut(df[biomarker], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
 
    # Get quartile cut points for labeling
    quartile_bins = pd.qcut(df[biomarker], q=4, retbins=True)[1]
    quartile_labels = {
        "Q1": f"Q1 ({quartile_bins[0]:.2f}–{quartile_bins[1]:.2f})",
        "Q2": f"Q2 ({quartile_bins[1]:.2f}–{quartile_bins[2]:.2f})",
        "Q3": f"Q3 ({quartile_bins[2]:.2f}–{quartile_bins[3]:.2f})",
        "Q4": f"Q4 ({quartile_bins[3]:.2f}–{quartile_bins[4]:.2f})",
    }
 
    print(f"\n{'='*55}")
    print(f"Quartile Analysis — {biomarker} vs {outcome_col}")
    print(f"{'='*55}")
 
    # ── 3. Summary stats per quartile ──────────────────────────────────────────
    summary = df.groupby("quartile", observed=True).agg(
        n            = (biomarker, "count"),
        mean_outcome = (outcome_col, "mean"),
        sd_outcome   = (outcome_col, "std"),
        n_cases      = (binary_col, "sum"),
    ).round(3)
    summary["pct_cases"] = (summary["n_cases"] / summary["n"] * 100).round(1)
    summary.index = [quartile_labels[q] for q in summary.index]
 
    print("\nSummary per Quartile:")
    print(summary.to_string())
 
    # ── 4. Correlation per quartile ────────────────────────────────────────────
    print("\nSpearman Correlation per Quartile:")
    corr_rows = []
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        subset = df[df["quartile"] == q][[biomarker, outcome_col]].dropna()
        if len(subset) > 10:
            corr, pval = stats.spearmanr(subset[biomarker], subset[outcome_col])
            corr_rows.append({
                "Quartile":    quartile_labels[q],
                "n":           len(subset),
                "Spearman r":  round(corr, 4),
                "p_value":     round(pval, 4),
                "significant": pval < 0.05
            })
    corr_df = pd.DataFrame(corr_rows).set_index("Quartile")
    print(corr_df.to_string())
 
    # ── 5. Logistic regression with Q1 as reference ───────────────────────────
    covariates = COVARIATES.copy()
    if filters and filters.get("sex"):
        covariates.remove("sex")
 
    df["quartile"] = pd.Categorical(df["quartile"], categories=["Q1","Q2","Q3","Q4"])
    formula = f"{binary_col} ~ C(quartile, Treatment('Q1')) + " + " + ".join(covariates)
    print(f"\nLogistic Formula: {formula}")
 
    logit_model = smf.logit(formula=formula, data=df).fit(disp=False)
 
    odds_df = pd.DataFrame({
        "odds_ratio": np.exp(logit_model.params),
        "ci_lower":   np.exp(logit_model.conf_int()[0]),
        "ci_upper":   np.exp(logit_model.conf_int()[1]),
        "p_value":    logit_model.pvalues
    }).round(4)
 
    # Keep only quartile rows
    quartile_or = odds_df[odds_df.index.str.contains("quartile")]
    quartile_or.index = ["Q2 vs Q1", "Q3 vs Q1", "Q4 vs Q1"]
 
    print("\nOdds Ratios vs Q1 (reference):")
    print(quartile_or.to_string())
 
    # ── 6. Linear regression per quartile ─────────────────────────────────────
    lm_formula = f"{outcome_col} ~ C(quartile, Treatment('Q1')) + " + " + ".join(covariates)
    lm_model   = smf.ols(formula=lm_formula, data=df).fit()
 
    lm_coefs = pd.DataFrame({
        "coef":    lm_model.params,
        "ci_lower": lm_model.conf_int()[0],
        "ci_upper": lm_model.conf_int()[1],
        "p_value":  lm_model.pvalues
    }).round(4)
 
    lm_quartile = lm_coefs[lm_coefs.index.str.contains("quartile")]
    lm_quartile.index = ["Q2 vs Q1", "Q3 vs Q1", "Q4 vs Q1"]
 
    print(f"\nLinear Regression Coefficients vs Q1 (R² = {lm_model.rsquared:.3f}):")
    print(lm_quartile.to_string())
 
    # ── 7. Visualizations ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
 
    # Bar chart — mean outcome per quartile
    q_labels  = [quartile_labels[q] for q in ["Q1", "Q2", "Q3", "Q4"]]
    means     = [df[df["quartile"] == q][outcome_col].mean() for q in ["Q1", "Q2", "Q3", "Q4"]]
    sds       = [df[df["quartile"] == q][outcome_col].std()  for q in ["Q1", "Q2", "Q3", "Q4"]]
 
    axes[0].bar(q_labels, means, yerr=sds, capsize=5,
                color=["#4C72B0", "#55A868", "#C44E52", "#8172B2"], alpha=0.8)
    axes[0].set_title(f"Mean {outcome_col} by {biomarker} Quartile", fontsize=12)
    axes[0].set_xlabel(f"{biomarker} Quartile")
    axes[0].set_ylabel(f"Mean {outcome_col}")
    axes[0].tick_params(axis='x', rotation=15)
 
    # Forest plot — ORs per quartile
    q_compare = ["Q2 vs Q1", "Q3 vs Q1", "Q4 vs Q1"]
    ors        = quartile_or["odds_ratio"].values
    ci_lower   = quartile_or["ci_lower"].values
    ci_upper   = quartile_or["ci_upper"].values
    y_pos      = range(len(q_compare))
 
    axes[1].errorbar(
        ors, y_pos,
        xerr=[ors - ci_lower, ci_upper - ors],
        fmt="o", color="steelblue", capsize=5, markersize=8
    )
    axes[1].axvline(x=1, color="red", linestyle="--", linewidth=1)
    axes[1].set_yticks(list(y_pos))
    axes[1].set_yticklabels(q_compare)
    axes[1].set_xlabel("Odds Ratio (95% CI)")
    axes[1].set_title(f"OR for Obesity by {biomarker} Quartile\n(Q1 = reference)", fontsize=12)
 
    # Annotate ORs on forest plot
    for i, (or_val, lo, hi) in enumerate(zip(ors, ci_lower, ci_upper)):
        axes[1].text(hi + 0.05, i, f"{or_val:.2f} ({lo:.2f}–{hi:.2f})",
                     va="center", fontsize=9)
 
    fig.suptitle(f"{biomarker} Quartile Analysis — {config['label']}", fontsize=13)
    plt.tight_layout()
    plt.show()
 
    return summary, quartile_or