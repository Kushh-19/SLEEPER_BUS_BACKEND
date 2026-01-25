# Prediction Approach: Waitlist Confirmation Probability

## 1. Project Overview
This module implements a **Confirmation Booking Prediction** feature for the Sleeper Bus Booking System. The goal is to provide waitlisted users with a real-time probability estimate (percentage) that their ticket will be confirmed before the journey date.

**Prediction Target:** $P(Confirmation | WaitlistPosition, Time, Route)$

---

## 2. Prediction Methodology
Since real-time historical booking data is unavailable for this assignment, we have implemented a **Simulated Model** (Mock Logic) that mimics the behavior of a supervised machine learning classifier.

### Model Choice: Logistic Regression (Simulated)
We simulated the output of a **Logistic Regression** model.
* **Reason for Choice:** Logistic Regression is the industry standard for binary classification problems (Confirmed vs. Not Confirmed) where the output needs to be a specific probability score between 0 and 1 (0% to 100%).
* **Alternative Considered:** Gradient Boosting (XGBoost) – rejected for this prototype due to high computational overhead for a simple mock API.

---

## 3. Feature Engineering & Logic
The prediction engine uses a **Heuristic Weighting System** derived from domain knowledge of travel patterns. The logic assumes the presence of a trained model with the following feature weights:

### A. Waitlist Position (Queue Depth)
* **Correlation:** Negative Strong
* **Logic:** The deeper the queue, the lower the chance of confirmation.
* **Weight:** `-5%` probability per position.
* **Reasoning:** A user at WL #1 only needs one cancellation to clear. A user at WL #20 needs twenty cancellations, which is statistically unlikely.

### B. Days to Departure (Time Decay)
* **Correlation:** Positive (Logarithmic)
* **Logic:** More time remaining implies a higher "cancellation window" for other passengers.
* **Weight:** * `> 10 Days`: +10% Bonus (High opportunity for clearance).
    * `< 2 Days`: -40% Penalty (Chart preparation imminent).

### C. Route Distance
* **Correlation:** Negative
* **Logic:** Long-distance travelers (Ahmedabad → Mumbai) show higher commitment and lower cancellation rates compared to short-hop travelers.
* **Weight:** -10% for full-length journeys.

---

## 4. Mock Training Dataset
The model simulation is based on the schema defined in `mock_booking_data.csv` included in this repository.

**Dataset Schema:**
| Feature | Type | Description |
| :--- | :--- | :--- |
| `booking_id` | String | Unique Identifier |
| `waitlist_position` | Integer | The user's position in the queue at booking time |
| `days_before_travel` | Integer | Number of days between booking and travel |
| `route_category` | Categorical | 'Long' (Ahd-Mum) or 'Short' (Ahd-Vad) |
| `outcome` | Binary | 1 (Confirmed) or 0 (Cancelled/Waitlist) |

**Training Assumption:** The weights used in `prediction_engine.py` represent the coefficients ($\beta$) that would have been learned by training on this dataset.

---

## 5. Final Output & usage
The API endpoint `/predict_confirmation` aggregates these weights to return a final percentage.

**Example Output:**
```json
{
  "confirmation_probability": "75%",
  "details": {
    "probability": 75,
    "confidence_score": "High",
    "drivers": {
      "queue_impact": -10,
      "time_impact": "Positive"
    }
  }
}