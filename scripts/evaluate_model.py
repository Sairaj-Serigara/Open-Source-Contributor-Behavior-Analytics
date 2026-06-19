import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("data/processed/contributors_processed.csv")

# Features
X = df[["contributions", "days_since_last_commit"]]
y = df["status"]

# Encode labels (IMPORTANT FIX)
le = LabelEncoder()
y_encoded = le.fit_transform(y)  
# Active = 0/1 depending on alphabet order

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Load model
model = joblib.load("outputs/best_model.pkl")

# Predict
y_pred = model.predict(X_test)

# Evaluation
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))