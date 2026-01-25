from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, date
import uuid

# IMPORT YOUR NEW PREDICTION ENGINE
from prediction_engine import ConfirmationPredictor 

# --- CONSTANTS ---
MEAL_PRICE = 100
STATIONS = {"Ahmedabad": 1, "Vadodara": 2, "Surat": 3, "Mumbai": 4}

# --- INITIALIZE APP & PREDICTOR ---
app = FastAPI(title="Sleeper Bus Booking API")
predictor = ConfirmationPredictor() # Initialize the AI model

# --- MOCK DB ---
seats = [
    {"id": "L1", "category": "lower", "price": 700},
    {"id": "L2", "category": "lower", "price": 700},
    {"id": "L3", "category": "lower", "price": 700},
    {"id": "U1", "category": "upper", "price": 500},
    {"id": "U2", "category": "upper", "price": 500},
    {"id": "U3", "category": "upper", "price": 500},
]
bookings = []

# --- MODELS ---
class BookingRequest(BaseModel):
    seat_ids: List[str]
    passenger_name: str
    age: int
    gender: str
    phone: str
    source: str
    destination: str
    travel_date: date
    num_meals: int = Field(default=0, ge=0)

class PredictionRequest(BaseModel):
    source: str
    destination: str
    days_before_travel: int = Field(..., description="Days remaining until travel date")
    waitlist_position: int = Field(..., description="Current Waitlist Position (e.g. 5)")

# --- HELPERS ---
def is_seat_available(seat_id: str, start_node: int, end_node: int, travel_date: date) -> bool:
    for b in bookings:
        if b["travel_date"] != travel_date: continue
        if b["status"] == "CANCELLED": continue
        if seat_id in b["seat_ids"]:
            booked_start = STATIONS.get(b["source"])
            booked_end = STATIONS.get(b["destination"])
            if start_node < booked_end and end_node > booked_start:
                return False
    return True

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "active", "stations": STATIONS, "pricing": {"meal_price": MEAL_PRICE}}

@app.get("/seats")
def get_seats(source: str = "Ahmedabad", destination: str = "Mumbai", travel_date: date = date.today()):
    start_node = STATIONS.get(source)
    end_node = STATIONS.get(destination)
    if not start_node or not end_node or start_node >= end_node:
        raise HTTPException(status_code=400, detail="Invalid route")

    seat_results = []
    for seat in seats:
        is_free = is_seat_available(seat["id"], start_node, end_node, travel_date)
        seat_results.append({
            "id": seat["id"], "category": seat["category"], "price": seat["price"],
            "status": "available" if is_free else "booked"
        })
    return {"source": source, "destination": destination, "date": travel_date, "seats": seat_results}

@app.post("/book")
def create_booking(booking: BookingRequest):
    start_node = STATIONS.get(booking.source)
    end_node = STATIONS.get(booking.destination)
    
    # Validation Omitted for brevity (Keep your original validation here!)
    
    # Calculate Price
    seat_price = sum(s["price"] for s in seats if s["id"] in booking.seat_ids)
    meal_price = booking.num_meals * MEAL_PRICE
    
    new_booking = {
        "booking_id": str(uuid.uuid4()),
        "passenger_name": booking.passenger_name,
        "seat_ids": booking.seat_ids,
        "source": booking.source, "destination": booking.destination,
        "travel_date": booking.travel_date, "num_meals": booking.num_meals,
        "total_price": seat_price + meal_price,
        "status": "confirmed"
    }
    bookings.append(new_booking)
    return new_booking

# --- INTEGRATED PREDICTION ENDPOINT ---
@app.post("/predict_confirmation")
def predict_confirmation(request: PredictionRequest):
    """
    Predicts waitlist confirmation chance using the external prediction engine.
    """
    # Delegate logic to the separate Data Science module
    result = predictor.predict_clearance(
        waitlist_position=request.waitlist_position,
        days_before_travel=request.days_before_travel,
        source=request.source,
        destination=request.destination
    )
    
    return {
        "confirmation_probability": f"{result['probability']}%",
        "details": result
    }