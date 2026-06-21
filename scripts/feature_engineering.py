import os
import pandas as pd

contributors = pd.read_csv("data/raw/contributors_raw.csv")
commits = pd.read_csv("data/raw/commits.csv")  # <-- IMPORTANT
prs = pd.read_csv("data/raw/contributor_prs.csv")
issues = pd.read_csv("data/raw/contributor_issues.csv")

# Merge everything
df = contributors.merge(commits, on=["repository", "username"], how="left")

df = df.merge(prs, on=["repository", "username"], how="left")

df = df.merge(issues, on=["repository", "username"], how="left")

# Fill numeric columns
numeric_cols = [
    "recent_commits",
    "avg_gap_days",
    "commit_frequency",
    "prs_opened",
    "prs_merged",
    "merge_rate",
    "issues_opened",
    "issues_closed",
    "issue_close_rate",
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(0)

# Fill date columns
date_cols = [
    "first_commit",
    "last_commit",
    "first_pr",
    "last_pr",
    "first_issue",
    "last_issue",
]

for col in date_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Never")

os.makedirs("data/processed", exist_ok=True)

df.to_csv("data/processed/contributor_features.csv", index=False)

print(df.columns.tolist())
print(df.shape)
