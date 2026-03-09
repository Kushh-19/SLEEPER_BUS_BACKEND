"""
Waitlist confirmation probability predictor.

Uses a trained Logistic Regression model (trained on historical clearance data).
Features: waitlist_position, days_before_travel, route_category (Long = Ahmedabad–Mumbai).
"""
import os
import joblib
import pandas as pd
from app.core.config import LONG_ROUTE_SOURCE, LONG_ROUTE_DESTINATION

DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(DIR, "model.pkl")


class ConfirmationPredictor:
    """
    Predicts the probability that a waitlisted ticket will be confirmed,
    using a trained sklearn Logistic Regression model.
    """

    def __init__(self):
        self._artifact = None
        self._load_model()

    def _load_model(self):
        if os.path.isfile(MODEL_PATH):
            self._artifact = joblib.load(MODEL_PATH)
        else:
            self._artifact = None

    def _route_category(self, source: str, destination: str) -> str:
        if source == LONG_ROUTE_SOURCE and destination == LONG_ROUTE_DESTINATION:
            return "Long"
        return "Short"

    def _route_encoded(self, source: str, destination: str) -> int:
        return 1 if self._route_category(source, destination) == "Long" else 0

    def predict_clearance(
        self,
        waitlist_position: int,
        days_before_travel: int,
        source: str,
        destination: str,
    ) -> dict:
        """
        Returns probability (0–100) that the waitlisted booking will be confirmed,
        with confidence and driver breakdown.
        """
        if self._artifact is None:
            return self._fallback_predict(waitlist_position, days_before_travel, source, destination)

        model = self._artifact["model"]
        route_enc = self._route_encoded(source, destination)
        cols = self._artifact["feature_names"]
        X = pd.DataFrame([[waitlist_position, days_before_travel, route_enc]], columns=cols)
        proba = model.predict_proba(X)[0]
        # Index 1 = confirmed class
        probability = int(round(proba[1] * 100))
        probability = max(0, min(100, probability))

        # Simple drivers for explainability
        queue_impact = -min(5 * waitlist_position, 50)
        time_impact = "Positive" if days_before_travel > 7 else ("Negative" if days_before_travel < 3 else "Neutral")
        confidence = "High" if (probability >= 70 or probability <= 30) else "Medium"

        return {
            "probability": probability,
            "confidence_score": confidence,
            "drivers": {
                "queue_impact": queue_impact,
                "time_impact": time_impact,
                "route_category": self._route_category(source, destination),
            },
        }

    def _fallback_predict(
        self,
        waitlist_position: int,
        days_before_travel: int,
        source: str,
        destination: str,
    ) -> dict:
        """Rule-based fallback when no trained model is present."""
        score = 100.0
        score -= 4 * waitlist_position
        if days_before_travel > 10:
            score += 5
        elif days_before_travel < 2:
            score -= 35
        elif days_before_travel < 5:
            score -= 15
        if self._route_category(source, destination) == "Long":
            score -= 8
        probability = max(0, min(99, int(score)))
        return {
            "probability": probability,
            "confidence_score": "Medium",
            "drivers": {
                "queue_impact": -4 * waitlist_position,
                "time_impact": "Positive" if days_before_travel > 7 else "Negative",
                "route_category": self._route_category(source, destination),
            },
        }
