from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse, CancelBookingRequest
from app.services.booking_service import (
    create_booking as svc_create,
    cancel_booking as svc_cancel,
    get_booking_by_booking_id,
    list_bookings as svc_list,
)

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse)
def create_booking(body: BookingCreate, db: Session = Depends(get_db)):
    try:
        booking = svc_create(
            db=db,
            passenger_name=body.passenger_name,
            age=body.age,
            gender=body.gender,
            phone=body.phone,
            seat_ids=body.seat_ids,
            source=body.source,
            destination=body.destination,
            travel_date=body.travel_date,
            num_meals=body.num_meals,
            waitlist_position=body.waitlist_position,
        )
        return booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel")
def cancel_booking(body: CancelBookingRequest, db: Session = Depends(get_db)):
    try:
        booking = svc_cancel(db=db, booking_id=body.booking_id)
        return {"message": "Booking cancelled successfully", "booking_id": booking.booking_id, "status": booking.status}
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[BookingResponse])
def list_bookings(
    travel_date: date | None = None,
    status: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    return svc_list(db=db, travel_date=travel_date, status=status, limit=limit)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str, db: Session = Depends(get_db)):
    booking = get_booking_by_booking_id(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
