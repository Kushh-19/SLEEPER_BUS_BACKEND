import uuid
from datetime import date
from sqlalchemy.orm import Session

from app.db.models import Booking
from app.core.config import STATIONS, SEAT_IDS
from app.services.seat_service import is_seat_available
from app.services.pricing_service import compute_booking_total, validate_seat_ids


def create_booking(
    db: Session,
    passenger_name: str,
    age: int,
    gender: str,
    phone: str,
    seat_ids: list[str],
    source: str,
    destination: str,
    travel_date: date,
    num_meals: int = 0,
    waitlist_position: int | None = None,
) -> Booking:
    ok, err = validate_seat_ids(seat_ids)
    if not ok:
        raise ValueError(err)

    start_node = STATIONS.get(source)
    end_node = STATIONS.get(destination)
    if not start_node or not end_node or start_node >= end_node:
        raise ValueError("Invalid route: source and destination must be valid and source before destination")

    # If not waitlisted, check all seats are available
    if waitlist_position is None:
        for sid in seat_ids:
            if not is_seat_available(db, sid, source, destination, travel_date):
                raise ValueError(f"Seat {sid} is not available for this route and date")

    total_price = compute_booking_total(seat_ids, num_meals)
    status = "WAITLISTED" if waitlist_position is not None else "CONFIRMED"
    booking_id = str(uuid.uuid4())

    booking = Booking(
        booking_id=booking_id,
        passenger_name=passenger_name,
        age=age,
        gender=gender,
        phone=phone,
        seat_ids=",".join(seat_ids),
        source=source,
        destination=destination,
        travel_date=travel_date,
        num_meals=num_meals,
        total_price=total_price,
        status=status,
        waitlist_position=waitlist_position,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking_id: str) -> Booking:
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        raise ValueError("Booking not found")
    if booking.status == "CANCELLED":
        raise ValueError("Booking is already cancelled")
    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_booking_id(db: Session, booking_id: str) -> Booking | None:
    return db.query(Booking).filter(Booking.booking_id == booking_id).first()


def get_booking_by_id(db: Session, id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.id == id).first()


def list_bookings(
    db: Session,
    travel_date: date | None = None,
    status: str | None = None,
    limit: int = 50,
) -> list[Booking]:
    q = db.query(Booking)
    if travel_date is not None:
        q = q.filter(Booking.travel_date == travel_date)
    if status is not None:
        q = q.filter(Booking.status == status)
    return q.order_by(Booking.id.desc()).limit(limit).all()
