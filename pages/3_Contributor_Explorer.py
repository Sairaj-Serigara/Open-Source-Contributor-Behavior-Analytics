import streamlit as st
import pandas as pd
from utils.dashboard_utils import repository_filter

st.title("👤 Contributor Explorer")
df = pd.read_csv("data/processed/contributor_features.csv")
df = repository_filter(df)


selected = st.selectbox(
    "🔍 Search or Select Contributor",
    sorted(df["username"].unique()),
    index=None,
    placeholder="Type a contributor name...",
)

if selected is None:
    st.info("Search and select a contributor to view details.")
    st.stop()

person = df[df["username"] == selected].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Repository", person["repository"])
    st.metric("Total Contributions", int(person["contributions"]))
    st.metric("Recent Commits", int(person["recent_commits"]))
    st.metric("Commit Frequency", round(person["commit_frequency"], 2))

with col2:
    st.metric("PRs Opened", int(person["prs_opened"]))
    st.metric("PRs Merged", int(person["prs_merged"]))
    st.metric("Merge Rate", round(person["merge_rate"], 2))
    st.metric("Issues Opened", int(person["issues_opened"]))

st.divider()

st.subheader("Dates")

st.write("**First Commit:**", person["first_commit"])
st.write("**Last Commit:**", person["last_commit"])
st.write("**First PR:**", person["first_pr"])
st.write("**Last PR:**", person["last_pr"])
st.write("**First Issue:**", person["first_issue"])
st.write("**Last Issue:**", person["last_issue"])
