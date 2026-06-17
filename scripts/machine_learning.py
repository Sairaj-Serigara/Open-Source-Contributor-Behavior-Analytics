import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("data/processed/contributors_processed.csv")

# Remove rows with missing values
df = df.dropna()

print(df.head())

# Convert target to numeric
df["status"] = df["status"].map({
    "Active": 1,
    "Inactive": 0
})

# Check for missing values
print("\nMissing Values")
print(df.isna().sum())

# ---------------------------------------------------
# Features & Target
# ---------------------------------------------------

X = df[
    [
        "contributions",
        "days_since_last_commit"
    ]
]

y = df["status"]

# ---------------------------------------------------
# Train/Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------------------------------------------
# Logistic Regression
# ---------------------------------------------------

model = LogisticRegression()

model.fit(
    X_train,
    y_train
)

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n" + "=" * 50)
print("LOGISTIC REGRESSION")
print("=" * 50)

print(f"Accuracy : {accuracy:.4f}")

print("\nConfusion Matrix")
print(confusion_matrix(
    y_test,
    predictions
))

print("\nClassification Report")
print(classification_report(
    y_test,
    predictions
))

# ---------------------------------------------------
# Random Forest
# ---------------------------------------------------

rf_model = RandomForestClassifier(
    random_state=42
)

rf_model.fit(
    X_train,
    y_train
)

rf_predictions = rf_model.predict(X_test)

rf_accuracy = accuracy_score(
    y_test,
    rf_predictions
)

print("\n" + "=" * 50)
print("RANDOM FOREST")
print("=" * 50)

print(f"Accuracy : {rf_accuracy:.4f}")

print("\nConfusion Matrix")
print(confusion_matrix(
    y_test,
    rf_predictions
))

print("\nClassification Report")
print(classification_report(
    y_test,
    rf_predictions
))

# ---------------------------------------------------
# Model Comparison
# ---------------------------------------------------

print("\n" + "=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

print(f"Logistic Regression : {accuracy:.4f}")
print(f"Random Forest       : {rf_accuracy:.4f}")

# ---------------------------------------------------
# Save Best Model
# ---------------------------------------------------

if rf_accuracy >= accuracy:
    best_model = rf_model
    best_name = "Random Forest"
else:
    best_model = model
    best_name = "Logistic Regression"

joblib.dump(
    best_model,
    "outputs/best_model.pkl"
)

print("\nBest Model :", best_name)
print("Model saved successfully to outputs/best_model.pkl")