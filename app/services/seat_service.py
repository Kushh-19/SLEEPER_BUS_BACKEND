from datetime import date
from sqlalchemy.orm import Session
from app.db.models import Booking
from app.core.config import STATIONS, SEATS


def is_seat_available(
    db: Session,
    seat_id: str,
    source: str,
    destination: str,
    travel_date: date
) -> bool:

    start_node = STATIONS.get(source)
    end_node = STATIONS.get(destination)

    if not start_node or not end_node or start_node >= end_node:
        return False

    bookings = db.query(Booking).filter(
        Booking.travel_date == travel_date,
        Booking.status != "CANCELLED"
    ).all()

    for booking in bookings:
        booked_start = STATIONS.get(booking.source)
        booked_end = STATIONS.get(booking.destination)

        if seat_id in booking.seat_ids.split(","):
            if start_node < booked_end and end_node > booked_start:
                return False

    return True


def get_available_seats(
    db: Session,
    source: str,
    destination: str,
    travel_date: date
):

    seat_results = []

    for seat in SEATS:
        available = is_seat_available(
            db,
            seat["id"],
            source,
            destination,
            travel_date
        )

        seat_results.append({
            "id": seat["id"],
            "category": seat["category"],
            "price": seat["price"],
            "status": "available" if available else "booked"
        })

    return seat_results
