import pandas as pd
from commits import get_last_commit
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_contributor(row):

    repository = row["repository"]
    username = row["username"]

    owner, repo = REPO_MAP[repository]

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):

        try:

            last_commit = get_last_commit(
                owner,
                repo,
                username
            )

            return {
                "repository": repository,
                "username": username,
                "contributions": row["contributions"],
                "last_commit": last_commit
            }

        except Exception as e:

            if attempt == MAX_RETRIES - 1:

                print(f"Failed: {username}")

                return {
                    "repository": repository,
                    "username": username,
                    "contributions": row["contributions"],
                    "last_commit": None
                }

            time.sleep(2)

# Mapping repository names to GitHub owner/repository
REPO_MAP = {
    "react": ("facebook", "react"),
    "vscode": ("microsoft", "vscode"),
    "tensorflow": ("tensorflow", "tensorflow")
}

# Read contributors
df = pd.read_csv("data/raw/contributors_raw.csv")

results = []

for index, row in df.iterrows():

    results = []

with ThreadPoolExecutor(max_workers=10) as executor:

    futures = [
        executor.submit(process_contributor, row)
        for _, row in df.iterrows()
    ]

    completed = 0

    for future in as_completed(futures):

        results.append(future.result())

        completed += 1

        if completed % 10 == 0 or completed == len(df):

            print(f"Processed {completed}/{len(df)} contributors...")

            pd.DataFrame(results).to_csv(
                "data/raw/contributor_commits.csv",
                index=False
            )

commit_df = pd.DataFrame(results)
commit_df = pd.DataFrame(results)

print("\nCollection Finished")
print(f"Total Contributors Processed : {len(commit_df)}")

print("\nSample Data")
print(commit_df.head())

print("\nDone!")