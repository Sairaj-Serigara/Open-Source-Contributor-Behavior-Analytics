import pandas as pd
from contributors import get_contributors
from github_api import github_get
from config import BASE_URL

REPOSITORIES = [
    ("facebook", "react"),
    ("tensorflow", "tensorflow"),
    ("microsoft", "vscode"),
]


def get_commit_history(owner, repo, username, max_commits=200):

    commits = []

    page = 1

    while len(commits) < max_commits:

        url = f"{BASE_URL}/repos/{owner}/{repo}/commits"

        params = {"author": username, "per_page": 100, "page": page}

        data = github_get(url, params)

        if not data:
            break

        commits.extend(data)

        if len(data) < 100:
            break

        page += 1

    return commits[:max_commits]


rows = []

for owner, repo in REPOSITORIES:

    print(f"\nRepository : {repo}")

    contributors = get_contributors(owner, repo)

    for contributor in contributors:

        username = contributor["username"]

        print("Collecting:", username)

        commits = get_commit_history(owner, repo, username)

        if len(commits) == 0:
            continue

        dates = [c["commit"]["author"]["date"] for c in commits]

        dates = sorted(pd.to_datetime(dates))

        first_commit = dates[0]
        last_commit = dates[-1]

        days_span = max((last_commit - first_commit).days, 1)

        commit_frequency = round(len(commits) / days_span, 3)

        gaps = []

        for i in range(1, len(dates)):
            gaps.append((dates[i] - dates[i - 1]).days)

        avg_gap = round(sum(gaps) / len(gaps), 2) if gaps else 0

        rows.append(
            {
                "repository": repo,
                "username": username,
                "recent_commits": len(commits),
                "first_commit": first_commit,
                "last_commit": last_commit,
                "avg_gap_days": avg_gap,
                "commit_frequency": commit_frequency,
            }
        )

df = pd.DataFrame(rows)

df.to_csv("data/raw/contributor_commits.csv", index=False)

print("\nSaved contributor_commits.csv")
print(df.head())
