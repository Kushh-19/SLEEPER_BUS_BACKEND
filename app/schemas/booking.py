from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict, Field


class BookingCreate(BaseModel):
    seat_ids: List[str] = Field(..., min_length=1, description="Seat IDs to book (e.g. L1, U2)")
    passenger_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=1, le=120)
    gender: str = Field(..., pattern="^(male|female|other)$")
    phone: str = Field(..., min_length=10, max_length=15)
    source: str = Field(..., description="Boarding station")
    destination: str = Field(..., description="Drop station")
    travel_date: date
    num_meals: int = Field(default=0, ge=0, description="Number of meals to add")
    waitlist_position: int | None = Field(default=None, ge=0, description="If waitlisted, position in queue")


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    booking_id: str
    passenger_name: str
    seat_ids: str
    source: str
    destination: str
    travel_date: date
    num_meals: int
    total_price: int
    status: str
    waitlist_position: int | None


class CancelBookingRequest(BaseModel):
    booking_id: str
