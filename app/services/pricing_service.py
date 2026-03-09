from typing import List
from app.core.config import SEATS, MEAL_PRICE, SEAT_IDS


def get_seat_price(seat_id: str) -> int | None:
    for s in SEATS:
        if s["id"] == seat_id:
            return s["price"]
    return None


def compute_booking_total(seat_ids: List[str], num_meals: int) -> int:
    total = 0
    for sid in seat_ids:
        p = get_seat_price(sid)
        if p is not None:
            total += p
    total += num_meals * MEAL_PRICE
    return total


def validate_seat_ids(seat_ids: List[str]) -> tuple[bool, str]:
    if not seat_ids:
        return False, "At least one seat is required"
    for sid in seat_ids:
        if sid not in SEAT_IDS:
            return False, f"Invalid seat id: {sid}"
    return True, ""
