import pandas as pd
from contributors import get_contributors

# GitHub repositories
REPOSITORIES = [
    ("facebook", "react"),
    ("microsoft", "vscode"),
    ("tensorflow", "tensorflow")
]

all_contributors = []

for owner, repo in REPOSITORIES:

    print(f"\nFetching contributors from {owner}/{repo}...")

    contributors = get_contributors(owner, repo, limit=50)

    print(f"Collected {len(contributors)} contributors")

    all_contributors.extend(contributors)

# Create DataFrame
df = pd.DataFrame(all_contributors)

print("\nSample Data")
print(df.head())

print(f"\nTotal Contributors : {len(df)}")

print("\nRepository-wise Count")
print(df["repository"].value_counts())

# Save CSV
df.to_csv(
    "data/raw/contributors_raw.csv",
    index=False
)

print("\nSaved to data/raw/contributors_raw.csv")