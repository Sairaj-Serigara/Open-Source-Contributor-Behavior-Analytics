import os
import time
import pandas as pd


import os
import sys

print("Current working directory:", os.getcwd())
print("\nPython search path:")
for p in sys.path:
    print(p)


from utils.github_api import get_recent_commits
from utils.helpers import commit_dates, average_gap_days, commit_frequency
from utils.logger import log

# -----------------------------
# GitHub repositories
# -----------------------------

OWNER = {"react": "facebook", "tensorflow": "tensorflow", "vscode": "microsoft"}

# -----------------------------
# Load contributors
# -----------------------------

contributors = pd.read_csv("data/raw/contributors_raw.csv")

# -----------------------------
# Resume Support
# -----------------------------

output_file = "data/raw/commits.csv"

completed = set()
results = []

if os.path.exists(output_file) and os.path.getsize(output_file) > 0:

    existing = pd.read_csv(output_file)

    completed = set(existing["username"])

    results = existing.to_dict("records")

    log(f"Resuming... {len(completed)} contributors already processed.")

# -----------------------------
# Start Timer
# -----------------------------

start = time.time()

total = len(contributors)

# -----------------------------
# Process Contributors
# -----------------------------

for i, row in contributors.iterrows():

    username = row["username"]

    repo = row["repository"]

    if username in completed:
        continue

    owner = OWNER[repo]

    log(f"[{i+1}/{total}] {username} ({repo})")

    commits = get_recent_commits(owner, repo, username)

    if len(commits) == 0:

        log("No commits found.")

        continue

    dates = commit_dates(commits)

    result = {
        "repository": repo,
        "username": username,
        "recent_commits": len(commits),
        "first_commit": dates[0],
        "last_commit": dates[-1],
        "avg_gap_days": average_gap_days(dates),
        "commit_frequency": commit_frequency(dates),
    }

    results.append(result)

    pd.DataFrame(results).to_csv(output_file, index=False)

# -----------------------------
# Finish
# -----------------------------

elapsed = time.time() - start

log(f"Finished in {elapsed:.2f} seconds")

log(f"Saved to {output_file}")
