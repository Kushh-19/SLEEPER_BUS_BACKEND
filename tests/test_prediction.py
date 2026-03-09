from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_predict_invalid_route():
    r = client.post(
        "/prediction/waitlist-confirmation",
        json={
            "source": "Mumbai",
            "destination": "Ahmedabad",
            "days_before_travel": 5,
            "waitlist_position": 2,
        },
    )
    assert r.status_code == 400
