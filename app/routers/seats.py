from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.db.database import get_db
from app.services.seat_service import get_available_seats
from app.core.config import STATIONS

router = APIRouter(prefix="/seats", tags=["Seats"])


@router.get("/")
def fetch_seats(
    source: str,
    destination: str,
    travel_date: date,
    db: Session = Depends(get_db)
):
    # Validate route
    start_node = STATIONS.get(source)
    end_node = STATIONS.get(destination)

    if not start_node or not end_node or start_node >= end_node:
        raise HTTPException(status_code=400, detail="Invalid route")

    seats = get_available_seats(
        db=db,
        source=source,
        destination=destination,
        travel_date=travel_date
    )

    return {
        "source": source,
        "destination": destination,
        "date": travel_date,
        "seats": seats
    }
