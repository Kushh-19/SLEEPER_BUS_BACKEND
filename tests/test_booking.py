from datetime import date, timedelta
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "active"
    assert "stations" in data


def test_seats_availability():
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    r = client.get("/seats/", params={"source": "Ahmedabad", "destination": "Mumbai", "travel_date": tomorrow})
    assert r.status_code == 200
    data = r.json()
    assert "seats" in data
    assert len(data["seats"]) == 6


def test_create_and_cancel_booking():
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    payload = {
        "seat_ids": ["L1"],
        "passenger_name": "Test User",
        "age": 30,
        "gender": "male",
        "phone": "9876543210",
        "source": "Ahmedabad",
        "destination": "Mumbai",
        "travel_date": tomorrow,
        "num_meals": 1,
    }
    r = client.post("/bookings/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "CONFIRMED"
    assert data["total_price"] == 700 + 100
    booking_id = data["booking_id"]

    r2 = client.post("/bookings/cancel", json={"booking_id": booking_id})
    assert r2.status_code == 200
    assert r2.json()["status"] == "CANCELLED"


def test_predict_waitlist_confirmation():
    r = client.post(
        "/prediction/waitlist-confirmation",
        json={
            "source": "Ahmedabad",
            "destination": "Mumbai",
            "days_before_travel": 10,
            "waitlist_position": 3,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "confirmation_probability" in data
    assert "probability_value" in data
    assert 0 <= data["probability_value"] <= 100
