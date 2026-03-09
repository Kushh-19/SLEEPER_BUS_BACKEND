from fastapi import APIRouter, HTTPException

from app.core.config import STATIONS
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.prediction.predictor import ConfirmationPredictor

router = APIRouter(prefix="/prediction", tags=["Waitlist prediction (ML)"])

predictor = ConfirmationPredictor()


@router.post("/waitlist-confirmation", response_model=PredictionResponse)
def predict_waitlist_confirmation(request: PredictionRequest):
    """
    Predicts the probability that a waitlisted ticket will be confirmed before travel.

    Uses a trained Logistic Regression model on historical clearance data.
    Features: waitlist position, days until travel, route (Long = Ahmedabad–Mumbai).
    """
    if STATIONS.get(request.source) is None or STATIONS.get(request.destination) is None:
        raise HTTPException(status_code=400, detail="Invalid source or destination")
    if STATIONS.get(request.source) >= STATIONS.get(request.destination):
        raise HTTPException(status_code=400, detail="Source must be before destination")

    result = predictor.predict_clearance(
        waitlist_position=request.waitlist_position,
        days_before_travel=request.days_before_travel,
        source=request.source,
        destination=request.destination,
    )
    return PredictionResponse(
        confirmation_probability=f"{result['probability']}%",
        probability_value=result["probability"],
        confidence_score=result["confidence_score"],
        details=result,
    )
