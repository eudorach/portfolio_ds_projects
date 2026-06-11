import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sys
sys.path.append("../..")
from nhanes_analysis import load_analysis_data, run_cohort_descriptives, run_biomarker_descriptives, run_distribution_plots, run_correlation, run_scatter, run_linear_regression, run_logistic_regression, run_quartile_analysis
from diagnosis_config import DISEASE_CONFIGS

# Database connection
DB_URI = 'sqlite:///nhanes_dashboard.db'
engine = create_engine(DB_URI)

# Load biomarker list from registry
@st.cache_data
def get_biomarkers():
    return pd.read_sql(
        "SELECT biomarker_name FROM biomarker_registry ORDER BY biomarker_name",
        engine
    )['biomarker_name'].tolist()

st.title("NHANES Biomarker Explorer")

# Sidebar
biomarker = st.sidebar.selectbox("Select Biomarker", get_biomarkers())
disease = st.sidebar.selectbox("Disease State", ["obesity", "hypertension", "diabetes"])

age_min, age_max = st.sidebar.slider("Age Range", 18, 80, (18, 65))
sex = st.sidebar.selectbox("Sex", ["All", "Male", "Female"])
exclude_diabetes = st.sidebar.checkbox("Exclude Diabetes")

# Build filters
filters = {"age_range": (age_min, age_max)}
if sex == "Male":
    filters["sex"] = 1
elif sex == "Female":
    filters["sex"] = 2
if exclude_diabetes:
    filters["exclude_diabetes"] = True

# Load data
@st.cache_data
def load_data(biomarker, disease, filters):
    return load_analysis_data(biomarker, disease, engine, filters=filters)

df = load_data(biomarker, disease, filters)
st.write(f"Cohort: {len(df):,} participants")

# Scatter plot
outcome_col = "bmi"
fig = px.scatter(
    df,
    x=biomarker,
    y=outcome_col,
    trendline="ols",
    title=f"{biomarker} vs {outcome_col}",
    opacity=0.4
)
st.plotly_chart(fig)

# Summary stats
st.subheader("Summary Statistics")
st.dataframe(df[[outcome_col, biomarker]].describe().round(3))