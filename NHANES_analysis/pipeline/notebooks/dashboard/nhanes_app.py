import streamlit as st
import pandas as pd
import plotly.express as px

#Importing existing functions

from sqlalchemy import create_engine, text
import sys
sys.path.append("../..")
from nhanes_analysis import load_analysis_data, run_cohort_descriptives, run_biomarker_descriptives, run_distribution_plots, run_correlation, run_scatter, run_linear_regression, run_logistic_regression, run_quartile_analysis
from diagnosis_config import DISEASE_CONFIGS
DB_URI = 'sqlite:///nhanes_dashboard.db'
engine = create_engine(DB_URI)

st.title("NHANES Biomarker Explorer")

#---------------
# SIDEBAR INPUTS
#---------------

biomarker = st.sidebar.selectbox(
    "Select Biomarker",
    ['glycohemoglobin']
)

disease_state = st.sidebar.selectbox(
    "Disease State",
    ['obesity']
)

#----------
# LOAD DATA
#----------

df = load_analysis_data(
    biomarker,
    'obesity',
    engine
)

st.write(f"Rows loaded: {len(df)}")

#--------------
# SCATTER PLOT
#--------------

fig = px.scatter(
    df,
    x='bmi',
    y=biomarker,
    trendline='ols',
    title=f"BMI vs {biomarker}"
)

st.plotly_chart(fig)

#-------------
# BASIC STATS
#-------------

st.subheader("Summary Statistics")

st.write(df[['bmi', biomarker]].describe())