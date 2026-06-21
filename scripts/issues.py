import pandas as pd
from collections import defaultdict

from utils.github_api import get_repository_issues

REPOSITORIES = [
    ("facebook", "react"),
    ("tensorflow", "tensorflow"),
    ("microsoft", "vscode"),
]

rows = []

for owner, repo in REPOSITORIES:

    print(f"\nRepository : {repo}")

    issues = get_repository_issues(owner, repo, max_issues=1000)

    print(f"Downloaded {len(issues)} issues")

    contributors = defaultdict(
        lambda: {
            "issues_opened": 0,
            "issues_closed": 0,
            "first_issue": None,
            "last_issue": None,
        }
    )

    for issue in issues:

        # Skip Pull Requests
        if "pull_request" in issue:
            continue

        if issue["user"] is None:
            continue

        username = issue["user"]["login"]

        contributors[username]["issues_opened"] += 1

        if issue["state"] == "closed":
            contributors[username]["issues_closed"] += 1

        created = issue["created_at"]

        if contributors[username]["first_issue"] is None:
            contributors[username]["first_issue"] = created

        contributors[username]["last_issue"] = created

    for username, stats in contributors.items():

        close_rate = 0

        if stats["issues_opened"] > 0:

            close_rate = round(stats["issues_closed"] / stats["issues_opened"] * 100, 2)

        rows.append(
            {
                "repository": repo,
                "username": username,
                "issues_opened": stats["issues_opened"],
                "issues_closed": stats["issues_closed"],
                "issue_close_rate": close_rate,
                "first_issue": stats["first_issue"],
                "last_issue": stats["last_issue"],
            }
        )

df = pd.DataFrame(rows)

df.to_csv("data/raw/contributor_issues.csv", index=False)

print("\nSaved contributor_issues.csv")

print(df.head())

print(df.shape)
