import os
import pandas as pd


# Load data

df = pd.read_csv("data/processed/contributor_features.csv")

# Repository summary

summary = (
    df.groupby("repository")
    .agg(
        contributors=("username", "nunique"),
        total_contributions=("contributions", "sum"),
        avg_recent_commits=("recent_commits", "mean"),
        avg_commit_frequency=("commit_frequency", "mean"),
        avg_gap_days=("avg_gap_days", "mean"),
        total_prs=("prs_opened", "sum"),
        merged_prs=("prs_merged", "sum"),
        avg_merge_rate=("merge_rate", "mean"),
        total_issues=("issues_opened", "sum"),
        closed_issues=("issues_closed", "sum"),
        avg_issue_close_rate=("issue_close_rate", "mean"),
    )
    .round(2)
    .reset_index()
)

# Overall repository score

summary["repository_score"] = (
    summary["avg_commit_frequency"] * 0.30
    + summary["avg_merge_rate"] * 0.30
    + summary["avg_issue_close_rate"] * 0.20
    + summary["avg_recent_commits"] * 0.20
).round(2)

summary = summary.sort_values("repository_score", ascending=False)

# Save

os.makedirs("outputs", exist_ok=True)
summary.to_csv("outputs/repository_summary.csv", index=False)
print("\nRepository Summary\n")
print(summary)

print("\nSaved -> outputs/repository_summary.csv")
