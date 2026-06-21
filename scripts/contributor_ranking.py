import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# -------------------------
# Load data
# -------------------------

df = pd.read_csv("data/processed/contributor_features.csv")

# -------------------------
# Metrics for ranking
# -------------------------

metrics = [
    "contributions",
    "recent_commits",
    "commit_frequency",
    "prs_merged",
    "merge_rate",
    "issues_closed",
    "issue_close_rate",
]

# -------------------------
# Normalize metrics
# -------------------------

scaler = MinMaxScaler()

df_scaled = df.copy()

df_scaled[metrics] = scaler.fit_transform(df[metrics])

# -------------------------
# Activity Score
# -------------------------

df_scaled["activity_score"] = (
    df_scaled["contributions"] * 0.25
    + df_scaled["recent_commits"] * 0.20
    + df_scaled["commit_frequency"] * 0.20
    + df_scaled["prs_merged"] * 0.15
    + df_scaled["merge_rate"] * 0.10
    + df_scaled["issues_closed"] * 0.05
    + df_scaled["issue_close_rate"] * 0.05
) * 100

df_scaled["activity_score"] = df_scaled["activity_score"].round(2)

# -------------------------
# Rank contributors
# -------------------------

ranking = df_scaled.sort_values("activity_score", ascending=False)

ranking.insert(0, "rank", range(1, len(ranking) + 1))

# -------------------------
# Save
# -------------------------

os.makedirs("outputs", exist_ok=True)

ranking.to_csv("outputs/contributor_ranking.csv", index=False)

print(ranking[["rank", "repository", "username", "activity_score"]].head(20))
