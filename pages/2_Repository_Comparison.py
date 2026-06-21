import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dashboard_utils import repository_filter

summary = pd.read_csv("outputs/repository_summary.csv")
# df = repository_filter(df)

st.title("🏆 Repository Comparison")

fig = px.bar(
    summary,
    x="repository",
    y="repository_score",
    color="repository",
    title="Repository Score",
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(summary)
