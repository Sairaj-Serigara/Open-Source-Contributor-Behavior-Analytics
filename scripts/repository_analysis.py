import pandas as pd

# -----------------------------
# Load master dataset
# -----------------------------

df = pd.read_csv(
    "data/processed/contributor_features.csv"
)

# -----------------------------
# Repository Summary
# -----------------------------

summary = df.groupby("repository").agg(

    contributors=("username", "nunique"),

    total_contributions=("contributions", "sum"),

    avg_commit_frequency=("commit_frequency", "mean"),

    avg_gap_days=("avg_gap_days", "mean"),

    prs_opened=("prs_opened", "sum"),

    prs_merged=("prs_merged", "sum"),

    avg_merge_rate=("merge_rate", "mean"),

    issues_opened=("issues_opened", "sum"),

    issues_closed=("issues_closed", "sum"),

    avg_issue_close_rate=("issue_close_rate", "mean")

).reset_index()

summary = summary.round(2)

summary.to_csv(
    "outputs/repository_summary.csv",
    index=False
)

print("\nRepository Summary\n")

print(summary)