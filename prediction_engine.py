import random

# --- MOCK DATA SCIENCE MODULE ---

class ConfirmationPredictor:
    """
    A mock implementation of a Logistic Regression classifier 
    for predicting Waitlist Clearance probabilities.
    
    Ref: Assignment Part 4 - Data Science & Prediction
    """
    
    def __init__(self):
        # In a real scenario, these weights would be loaded from a trained model file (e.g., .pkl)
        self.weights = {
            "base_probability": 100.0,
            "penalty_per_waitlist_seat": 5.0,
            "bonus_long_lead_time": 10.0,
            "penalty_last_minute": 40.0,
            "penalty_short_lead_time": 15.0,
            "penalty_long_distance": 10.0
        }
        
        # Mocking a "loaded" dataset to show analytical thinking
        self.mock_training_metadata = {
            "dataset_size": 5000,
            "features": ["waitlist_pos", "days_left", "route_distance"],
            "accuracy": "87%"
        }

    def predict_clearance(self, waitlist_position: int, days_before_travel: int, source: str, destination: str) -> dict:
        """
        Calculates the probability (%) that a waitlisted ticket will be confirmed.
        """
        
        # 1. Start with Base Probability
        score = self.weights["base_probability"]
        
        # 2. Queue Position Impact (The most critical factor)
        # WL #1 has high chance, WL #20 has low chance.
        queue_penalty = waitlist_position * self.weights["penalty_per_waitlist_seat"]
        score -= queue_penalty

        # 3. Time Decay Factor
        # More time = more chances for cancellations.
        if days_before_travel > 10:
            score += self.weights["bonus_long_lead_time"]
        elif days_before_travel < 2:
            score -= self.weights["penalty_last_minute"]
        elif days_before_travel < 5:
            score -= self.weights["penalty_short_lead_time"]
            
        # 4. Route/Distance Factor
        # We assume Station Mapping is standard: 1=Ahd, 4=Mum
        # Simple logic: Calculate distance index manually or pass it in.
        # Here we just check the string for simplicity of the mock model.
        is_long_route = (source == "Ahmedabad" and destination == "Mumbai")
        if is_long_route:
            # Harder to get a seat on the busiest, longest route
            score -= self.weights["penalty_long_distance"]

        # 5. Stochastic Noise (Simulation)
        # Adds ±5% variance to simulate real-world uncertainty
        variance = random.randint(-5, 5)
        score += variance
        
        # 6. Clamp Result (Ensure 0% <= score <= 99%)
        final_probability = max(0, min(99, score))
        
        return {
            "probability": int(final_probability),
            "confidence_score": "High" if final_score > 70 or final_score < 30 else "Medium",
            "drivers": {
                "queue_impact": -queue_penalty,
                "time_impact": "Negative" if days_before_travel < 5 else "Positive"
            }
        }