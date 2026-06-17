import pandas as pd

# Read processed data
df = pd.read_csv("data/processed/contributors_processed.csv")

print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print("\nTotal Contributors :", len(df))

print("\nRepository Count")
print(df["repository"].value_counts())

print("\nStatus Count")
print(df["status"].value_counts())

print("\n" + "=" * 60)
print("CONTRIBUTION STATISTICS")
print("=" * 60)

print(df["contributions"].describe())

print("\n" + "=" * 60)
print("DAYS SINCE LAST COMMIT")
print("=" * 60)

print(df["days_since_last_commit"].describe())


print("\n" + "=" * 60)
print("REPOSITORY-WISE CONTRIBUTIONS")
print("=" * 60)

print(
    df.groupby("repository")["contributions"].describe()
)


print("\n" + "=" * 60)
print("ACTIVE vs INACTIVE")
print("=" * 60)

print(
    df.groupby("status")["contributions"].describe()
)



df["status_numeric"] = df["status"].map({
    "Active": 1,
    "Inactive": 0
})


print("\n" + "=" * 60)
print("CORRELATION")
print("=" * 60)

print(
    df[
        [
            "contributions",
            "days_since_last_commit",
            "status_numeric"
        ]
    ].corr()
)


summary = df.describe(include="all")

summary.to_csv(
    "outputs/statistics_summary.csv"
)