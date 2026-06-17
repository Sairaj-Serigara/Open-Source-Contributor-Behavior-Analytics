import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Open Source Contributor Behavior Analytics",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv(
    "data/processed/contributors_processed.csv"
)

st.title("📊 Open Source Contributor Behavior Analytics")

st.dataframe(df)

st.title("📊 Open Source Contributor Behavior Analytics")

total = len(df)
active = len(df[df["status"] == "Active"])
inactive = len(df[df["status"] == "Inactive"])
repositories = df["repository"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contributors", total)
col2.metric("Active", active)
col3.metric("Inactive", inactive)
col4.metric("Repositories", repositories)

st.sidebar.title("Filters")

repo = st.sidebar.selectbox(
    "Repository",
    ["All"] + sorted(df["repository"].unique().tolist())
)

if repo != "All":
    filtered_df = df[df["repository"] == repo]
else:
    filtered_df = df

st.dataframe(filtered_df)