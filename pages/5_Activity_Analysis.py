import streamlit as st
import pandas as pd
import plotly.express as px

from utils.dashboard_utils import repository_filter

st.title("📊 Activity Analysis")

# Load data
df = pd.read_csv("outputs/contributor_activity.csv")

# Repository filter
df = repository_filter(df)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Average Score", round(df["activity_score"].mean(), 2))
c2.metric("Highest Score", round(df["activity_score"].max(), 2))
c3.metric("Lowest Score", round(df["activity_score"].min(), 2))
c4.metric("Total Contributors", len(df))
st.divider()

# Activity Distribution

counts = df["activity_level"].value_counts().reset_index()
counts.columns = ["Activity Level", "Count"]
fig = px.bar(
    counts,
    x="Activity Level",
    y="Count",
    color="Activity Level",
    text="Count",
    title="Contributor Activity Distribution",
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
# Average Activity Score by Repository
repo_scores = df.groupby("repository")["activity_score"].mean().reset_index()

fig2 = px.bar(
    repo_scores,
    x="repository",
    y="activity_score",
    color="repository",
    text_auto=".2f",
    title="Average Activity Score by Repository",
)

st.plotly_chart(fig2, use_container_width=True)
st.divider()
st.subheader("Activity Dataset")
st.dataframe(df, use_container_width=True)
