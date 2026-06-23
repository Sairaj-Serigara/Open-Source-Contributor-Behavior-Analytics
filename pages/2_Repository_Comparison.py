import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dashboard_utils import repository_filter

summary = pd.read_csv("outputs/repository_summary.csv")
summary = repository_filter(summary)
st.title("🏆 Repository Comparison")

fig = px.bar(
    summary,
    x="repository",
    y="repository_score",
    color="repository",
    title="Repository Score",
)

st.plotly_chart(fig, use_container_width=True)

repo = (
    summary.groupby("repository")["total_contributions"]
    .sum()
    .reset_index()
)

fig = px.pie(
    repo,
    names="repository",
    values="total_contributions",
    hole=0.55,
    title="share of total contribution made to each repository"
)

fig.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.dataframe(summary)