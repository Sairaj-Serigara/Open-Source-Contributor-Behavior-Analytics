import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

st.set_page_config(
    page_title="Open Source Contributor  Analytics",
    page_icon="📊",
    layout="wide"
)

df = pd.read_csv("data/processed/contributors_processed.csv")
model = joblib.load("outputs/best_model.pkl")

st.title("📊 Open Source Contributor  Analytics")

# -----------------------------
# Metrics
# -----------------------------

total = len(df)
active = len(df[df["status"] == "Active"])
inactive = len(df[df["status"] == "Inactive"])
repositories = df["repository"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contributors", total)
col2.metric("Active", active)
col3.metric("Inactive", inactive)
col4.metric("Repositories", repositories)

# -----------------------------
# Sidebar Filter
# -----------------------------

st.sidebar.title("Filters")

repo = st.sidebar.selectbox(
    "Repository",
    ["All"] + sorted(df["repository"].unique())
)

if repo == "All":
    filtered_df = df
else:
    filtered_df = df[df["repository"] == repo]


repo_summary = (
    df.groupby("repository")
    .agg(
        Contributors=("username", "count"),
        Active=("status", lambda x: (x == "Active").sum()),
        Inactive=("status", lambda x: (x == "Inactive").sum()),
        Avg_Contributions=("contributions", "mean"),
        Avg_Days=("days_since_last_commit", "mean")
    )
    .reset_index()
)

repo_summary["Active %"] = (
    repo_summary["Active"] /
    repo_summary["Contributors"] * 100
).round(1)

repo_summary["Inactive %"] = (
    repo_summary["Inactive"] /
    repo_summary["Contributors"] * 100
).round(1)

st.header("📊 Repository Comparison")

st.dataframe(
    repo_summary,
    use_container_width=True
)

fig_repo = px.bar(
    repo_summary,
    x="repository",
    y="Active %",
    color="repository",
    title="Active Contributors (%) by Repository"
)

st.plotly_chart(fig_repo, width="stretch")



fig_days = px.bar(
    repo_summary,
    x="repository",
    y="Avg_Days",
    color="repository",
    title="Average Days Since Last Commit"
)

st.plotly_chart(fig_days, width="stretch")

status_count = filtered_df["status"].value_counts().reset_index()
status_count.columns = ["Status", "Count"]

fig1 = px.bar(
    status_count,
    x="Status",
    y="Count",
    color="Status",
    title="Active vs Inactive Contributors"
)

repo_count = filtered_df["repository"].value_counts().reset_index()
repo_count.columns = ["Repository", "Contributors"]

fig2 = px.pie(
    repo_count,
    values="Contributors",
    names="Repository",
    title="Repository Distribution"
)


fig3 = px.histogram(
    filtered_df,
    x="contributions",
    nbins=20,
    title="Contribution Distribution"
)


fig4 = px.scatter(
    filtered_df,
    x="contributions",
    y="days_since_last_commit",
    color="status",
    hover_name="username",
    title="Contributor Activity"
)
# First row
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, width="stretch")

with col2:
    st.plotly_chart(fig2, width="stretch")


# Second row
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig3, width="stretch")

with col4:
    st.plotly_chart(fig4, width="stretch")


st.header("🤖 Contributor Activity Prediction")
col1, col2 = st.columns(2)

with col1:
    contributions = st.number_input(
        "Total Contributions",
        min_value=0,
        value=500
    )

with col2:
    days = st.number_input(
        "Days Since Last Commit",
        min_value=0,
        value=100
    )
if st.button("Predict Status"):

    input_data = pd.DataFrame({
        "contributions": [contributions],
        "days_since_last_commit": [days]
    })

    # st.write(input_data)

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]

    confidence = max(probability) * 100

    if prediction == 1:
        st.success(f"🟢 Predicted Status: Active ({confidence:.1f}% confidence)")
    else:
        st.error(f"🔴 Predicted Status: Inactive ({confidence:.1f}% confidence)")
# -----------------------------
# Dataset
# -----------------------------

st.subheader("Contributor Dataset")

st.dataframe(filtered_df, use_container_width=True)