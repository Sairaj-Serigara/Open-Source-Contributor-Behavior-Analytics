import streamlit as st
import pandas as pd
import plotly.express as px

from utils.dashboard_utils import repository_filter

st.title("🏆 Top Contributors")

# Load data
df = pd.read_csv("outputs/contributor_ranking.csv")

# Repository filter
df = repository_filter(df)

st.divider()

# User input
top_n = st.number_input(
    "Enter number of top contributors",
    min_value=1,
    max_value=len(df),
    value=min(10, len(df)),
    step=1,
)

if st.button("Show Top Contributors"):

    top = df.nlargest(int(top_n), "activity_score")

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Highest Score", round(top["activity_score"].max(), 2))
    c2.metric("Average Score", round(top["activity_score"].mean(), 2))
    c3.metric("Repositories", top["repository"].nunique())

    st.divider()
    # Chart
    fig = px.bar(
        top,
        x="activity_score",
        y="username",
        color="repository",
        orientation="h",
        text="activity_score",
        title=f"Top {int(top_n)} Contributors",
    )

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="Activity Score",
        yaxis_title="Contributor",
    )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.subheader("Contributor Ranking")
    st.dataframe(top, use_container_width=True)
