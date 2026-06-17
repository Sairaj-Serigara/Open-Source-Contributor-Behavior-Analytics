import pandas as pd
import matplotlib.pyplot as plt

# Read processed data
df = pd.read_csv("data/processed/contributors_processed.csv")

print(df.head())

status_counts = df["status"].value_counts()

plt.figure(figsize=(6,4))

status_counts.plot(kind="bar")

plt.title("Active vs Inactive Contributors")
plt.xlabel("Status")
plt.ylabel("Number of Contributors")

plt.tight_layout()

plt.savefig("outputs/charts/status_bar.png")

plt.show()


plt.figure(figsize=(6,6))

status_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.ylabel("")

plt.title("Contributor Status Distribution")

plt.savefig("outputs/charts/status_pie.png")

plt.show()


# Repository-wise Active vs Inactive

repo_status = pd.crosstab(
    df["repository"],
    df["status"]
)

plt.figure(figsize=(7,5))

repo_status.plot(
    kind="bar",
    stacked=True
)

plt.title("Repository-wise Contributor Status")
plt.xlabel("Repository")
plt.ylabel("Number of Contributors")

plt.tight_layout()

plt.savefig("outputs/charts/repository_status.png")

plt.show()



plt.figure(figsize=(7,5))

plt.hist(
    df["contributions"],
    bins=20
)

plt.title("Distribution of Contributions")
plt.xlabel("Number of Contributions")
plt.ylabel("Contributors")

plt.tight_layout()

plt.savefig("outputs/charts/contributions_histogram.png")

plt.show()



plt.figure(figsize=(7,5))

plt.scatter(
    df["contributions"],
    df["days_since_last_commit"]
)

plt.title("Contributions vs Days Since Last Commit")
plt.xlabel("Contributions")
plt.ylabel("Days Since Last Commit")

plt.tight_layout()

plt.savefig("outputs/charts/contribution_scatter.png")

plt.show()



# Repository-wise Active vs Inactive

repo_status = pd.crosstab(
    df["repository"],
    df["status"]
)

plt.figure(figsize=(8,5))

repo_status.plot(
    kind="bar",
    stacked=True
)

plt.title("Repository-wise Active vs Inactive Contributors")
plt.xlabel("Repository")
plt.ylabel("Number of Contributors")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("outputs/charts/repository_status.png")

plt.show()




# Contributions Histogram

plt.figure(figsize=(8,5))

plt.hist(
    df["contributions"],
    bins=20,
    edgecolor="black"
)

plt.title("Distribution of Contributions")
plt.xlabel("Number of Contributions")
plt.ylabel("Number of Contributors")

plt.tight_layout()

plt.savefig("outputs/charts/contributions_histogram.png")

plt.show()



# Scatter Plot

plt.figure(figsize=(8,5))

plt.scatter(
    df["contributions"],
    df["days_since_last_commit"]
)

plt.title("Contributions vs Days Since Last Commit")
plt.xlabel("Contributions")
plt.ylabel("Days Since Last Commit")

plt.tight_layout()

plt.savefig("outputs/charts/contribution_scatter.png")

plt.show()


# Days Since Last Commit Histogram

plt.figure(figsize=(8,5))

plt.hist(
    df["days_since_last_commit"],
    bins=20,
    edgecolor="black"
)

plt.title("Days Since Last Contribution")
plt.xlabel("Days")
plt.ylabel("Number of Contributors")

plt.tight_layout()

plt.savefig("outputs/charts/days_histogram.png")

plt.show()