from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    source: str = Field(..., description="Boarding station")
    destination: str = Field(..., description="Drop station")
    days_before_travel: int = Field(..., ge=0, description="Days remaining until travel date")
    waitlist_position: int = Field(..., ge=0, description="Current waitlist position (e.g. 5)")


class PredictionResponse(BaseModel):
    confirmation_probability: str  # e.g. "72%"
    probability_value: int
    confidence_score: str
    details: dict
