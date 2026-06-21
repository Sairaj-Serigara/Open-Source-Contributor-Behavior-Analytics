import os
import pandas as pd

df = pd.read_csv("outputs/contributor_ranking.csv")


def category(score):

    if score >= 80:
        return "Highly Active"

    elif score >= 60:
        return "Active"

    elif score >= 40:
        return "Moderately Active"

    elif score >= 20:
        return "Low Activity"

    else:
        return "At Risk"


df["activity_level"] = df["activity_score"].apply(category)

os.makedirs("outputs", exist_ok=True)

df.to_csv("outputs/contributor_activity.csv", index=False)

print(df[["rank", "username", "activity_score", "activity_level"]].head(20))

print("\n")

print(df["activity_level"].value_counts())
