import streamlit as st
import pandas as pd
from utils.dashboard_utils import repository_filter

df = pd.read_csv("data/processed/contributor_features.csv")
df = repository_filter(df)
st.title("📈 Overview")

import plotly.express as px

counts = df.groupby("repository").size().reset_index(name="contributors")

fig = px.bar(
    counts,
    x="repository",
    y="contributors",
    color="repository",
    title="Contributors by Repository",
)

st.plotly_chart(fig, use_container_width=True)

fig = px.box(
    df,
    x="repository",
    y="commit_frequency",
    color="repository",
    title="Commit Frequency Distribution",
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    df.groupby("repository")["merge_rate"].mean().reset_index(),
    x="repository",
    y="merge_rate",
    color="repository",
    title="Average Merge Rate",
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
st.subheader("Dataset")
st.dataframe(df)
