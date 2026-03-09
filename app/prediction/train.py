"""
Train a Logistic Regression model for waitlist confirmation probability.

Uses historical booking data: waitlist_position, days_before_travel, route_category (Long/Short).
Run from project root: python -m app.prediction.train
"""
import os
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Paths relative to this file
DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DIR, "data", "mock_booking_data.csv")
MODEL_PATH = os.path.join(DIR, "model.pkl")


def _encode_route(s: str) -> int:
    return 1 if s.strip().lower() == "long" else 0


def train():
    df = pd.read_csv(DATA_PATH)
    df["route_encoded"] = df["route_category"].map(_encode_route)

    X = df[["waitlist_position", "days_before_travel", "route_encoded"]]
    y = df["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", round(acc, 4))
    print(classification_report(y_test, y_pred))

    artifact = {
        "model": model,
        "feature_names": list(X.columns),
    }
    joblib.dump(artifact, MODEL_PATH)
    print("Model saved to", MODEL_PATH)


if __name__ == "__main__":
    train()
