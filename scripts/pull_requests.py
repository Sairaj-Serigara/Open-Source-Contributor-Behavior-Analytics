import pandas as pd
from collections import defaultdict
import json
import os

from utils.github_api import get_repository_pull_requests

REPOSITORIES = [
    ("facebook", "react"),
    ("tensorflow", "tensorflow"),
    ("microsoft", "vscode"),
]

rows = []

for owner, repo in REPOSITORIES:

    print(f"\nRepository : {repo}")

    prs = get_repository_pull_requests(owner, repo, max_prs=1000)

    os.makedirs("data/raw/pr_cache", exist_ok=True)

    with open(f"data/raw/pr_cache/{repo}_prs.json", "w", encoding="utf-8") as f:
        json.dump(prs, f, indent=2)

    print(f"Downloaded {len(prs)} PRs")

    contributors = defaultdict(
        lambda: {"prs_opened": 0, "prs_merged": 0, "first_pr": None, "last_pr": None}
    )

    # -----------------------------
    # Process every PR
    # -----------------------------
    for pr in prs:

        username = pr["user"]["login"]

        contributors[username]["prs_opened"] += 1

        if pr["merged_at"] is not None:
            contributors[username]["prs_merged"] += 1

        created = pr["created_at"]

        if contributors[username]["first_pr"] is None:
            contributors[username]["first_pr"] = created

        contributors[username]["last_pr"] = created

    # -----------------------------
    # Save contributor statistics
    # -----------------------------
    for username, stats in contributors.items():

        if stats["prs_opened"] > 0:
            merge_rate = round(stats["prs_merged"] / stats["prs_opened"] * 100, 2)
        else:
            merge_rate = 0

        rows.append(
            {
                "repository": repo,
                "username": username,
                "prs_opened": stats["prs_opened"],
                "prs_merged": stats["prs_merged"],
                "merge_rate": merge_rate,
                "first_pr": stats["first_pr"],
                "last_pr": stats["last_pr"],
            }
        )

# -----------------------------
# Save CSV
# -----------------------------
df = pd.DataFrame(rows)

df.to_csv("data/raw/contributor_prs.csv", index=False)

print("\nSaved contributor_prs.csv")
print(df.head())
print(df.shape)
