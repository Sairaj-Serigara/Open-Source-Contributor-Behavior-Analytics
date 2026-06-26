import pandas as pd
from datetime import datetime, timezone

# Read collected data
df = pd.read_csv("data/raw/contributor_commits.csv")

print("Original Shape :", df.shape)

# Remove duplicate contributors


df = df.drop_duplicates(subset=["repository", "username"])
print("After Removing Duplicates :", df.shape)

# Remove missing usernames

df = df.dropna(subset=["username"])

# Remove bots

df = df[~df["username"].str.contains("bot", case=False, na=False)]
print("After Removing Bots :", df.shape)

# Convert last_commit to datetime

df["last_commit"] = pd.to_datetime(df["last_commit"], utc=True)

# Calculate days since last contribution

today = datetime.now(timezone.utc)
df["days_since_last_commit"] = (today - df["last_commit"]).dt.days


# Contributor Status


df["status"] = df["days_since_last_commit"].apply(
    lambda x: "Inactive" if x > 365 else "Active"
)

# Save cleaned data

df.to_csv("data/processed/contributors_processed.csv", index=False)

print("\nProcessed Data")
print(df.head())

print("\nStatus Count")
print(df["status"].value_counts())

print("\nSaved to data/processed/contributors_processed.csv")
