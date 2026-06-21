import streamlit as st


def repository_filter(df):

    repo = st.sidebar.selectbox(
        "📂 Repository",
        ["All"] + sorted(df["repository"].unique()),
        key="repository_filter",
    )

    if repo == "All":
        return df

    return df[df["repository"] == repo]
