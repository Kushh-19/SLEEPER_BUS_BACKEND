# Sleeper Bus Booking System (Ahmedabad → Mumbai)

## Project Overview

This project is a web-based sleeper bus booking system designed for a **single sleeper bus service** operating between **Ahmedabad and Mumbai**, with intermediate stations such as **Vadodara** and **Surat**.

The system includes an **interactive seat booking flow**, an **integrated meal booking service**, and an **AI-powered waitlist confirmation prediction engine** that estimates the likelihood of booking confirmation in percentage terms.

---

## UI/UX Prototype

**Figma Prototype Link:**  
[https://www.figma.com/proto/FgrwKbxB00Raaq4S9a7Bpf/Sleeper-Bus-Booking-%E2%80%93-Prototype?node-id=3-2572&p=f&t=Qmtna1Qo2SXS8IF9-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=3%3A2572]

---

## Core Features (Web Flow)

### 1. Smart Route & Seat Availability Logic
- Users can select source and destination stations, including intermediate stops.
- Seat availability is calculated per route segment to prevent overlapping seat conflicts.
- Example: A seat booked from Ahmedabad → Vadodara remains available for Vadodara → Mumbai.

---

### 2. Interactive Sleeper Seat Layout
- Logical separation between Lower Deck and Upper Deck seats.
- Clear seat status handling (Available / Booked).
- Backend structure supports UI visualization.

---

### 3. Integrated Meal Booking (Unique Requirement)
- Users can add meals during the seat booking process.
- Meal cost is calculated dynamically and added to the total fare.
- Total Fare = Seat Price + Meal Price.

---

### 4. AI-Powered Booking Confirmation Prediction
- For waitlisted scenarios, users can check a **Confirmation Probability (%)**.
- Prediction considers:
  - Waitlist position
  - Days before travel
  - Route demand (busy vs shorter routes)

---

### 5. Real-Time Booking Conflict Prevention
- Prevents double booking of seats on overlapping routes.
- Seat availability is validated at booking time.

---

### 6. Seamless Booking Cancellation
- Users can cancel bookings using a booking ID.
- Cancelled bookings immediately release seats back into availability.

---

## User Flow Summary

1. User selects source, destination, and travel date.
2. System displays available seats.
3. User selects seat(s) and optional meal(s).
4. Booking is confirmed with total fare.
5. User may cancel booking or check waitlist confirmation probability.

---

## Critical Test Cases

### A. Functional Test Cases

1. **Route Validation**
   - Searching for an invalid route (e.g., Mumbai → Ahmedabad) returns an error.

2. **Price Calculation**
   - 1 Seat (₹700) + 2 Meals (₹200) → Total should be ₹900.

3. **Seat Booking Persistence**
   - After booking, the seat appears as booked for subsequent users.

4. **Cancellation Flow**
   - Cancelling a booking updates status to CANCELLED and releases seats.

---

### B. Edge Cases

1. **Segment Overlap Handling**
   - Seat booked Ahmedabad → Vadodara must remain available for Vadodara → Mumbai.

2. **Last-Minute Prediction**
   - Prediction made < 2 days before travel returns very low probability.

3. **Concurrent Booking Requests**
   - Two simultaneous booking requests for the same seat result in only one success.

4. **Invalid Meal Count**
   - Negative meal values return validation errors.

---

### C. UI/UX Validation Cases

1. Clear distinction between available and booked seats.
2. User-friendly error messages instead of raw server errors.
3. Confirmation probability displayed clearly as a percentage.

---

## Backend API Overview

### Tech Stack
- **Backend:** Python (FastAPI)
- **Database:** SQLite + SQLAlchemy ORM
- **Validation:** Pydantic
- **ML:** scikit-learn (Logistic Regression) for waitlist confirmation prediction

### Project Structure
```
app/
  core/       # Config (stations, seats, meal price)
  db/         # Database engine, models, get_db
  routers/    # booking, seats, prediction
  schemas/    # Pydantic request/response models
  services/   # booking_service, seat_service, pricing_service
  prediction/ # ML model (train.py, predictor.py), data/, model.pkl
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info and stations |
| GET | `/health` | Health check |
| GET | `/seats/` | Available seats (query: source, destination, travel_date) |
| POST | `/bookings/` | Create booking (body: seat_ids, passenger details, source, destination, travel_date, num_meals, optional waitlist_position) |
| POST | `/bookings/cancel` | Cancel booking (body: booking_id) |
| GET | `/bookings` | List bookings (optional: travel_date, status, limit) |
| GET | `/bookings/{booking_id}` | Get one booking |
| POST | `/prediction/waitlist-confirmation` | ML prediction for waitlist confirmation % (body: source, destination, days_before_travel, waitlist_position) |

---

## Waitlist Confirmation Prediction (ML)

### Goal
Estimate the **probability (%)** that a waitlisted ticket will be confirmed before travel.

### Implementation
- **Model:** Logistic Regression (scikit-learn) trained on historical clearance data.
- **Features:** `waitlist_position`, `days_before_travel`, `route_category` (Long = Ahmedabad–Mumbai, Short = other segments).
- **Training data:** `app/prediction/data/mock_booking_data.csv` (150 records). Retrain with:
  ```bash
  python -m app.prediction.train
  ```
- **Fallback:** If `model.pkl` is missing, a rule-based heuristic is used.

### Output
- `confirmation_probability` (e.g. "72%")
- `probability_value` (0–100)
- `confidence_score` (High/Medium)
- `details.drivers`: queue_impact, time_impact, route_category

See **PREDICTION_APPROACH.md** for more detail.

---

## System Assumptions

- Single bus; static station list (Ahmedabad, Vadodara, Surat, Mumbai).
- No payment gateway or user authentication.
- SQLite DB file: `./sleeper_bus.db`.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Train the waitlist prediction model:
   ```bash
   python -m app.prediction.train
   ```
3. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. API docs: **http://127.0.0.1:8000/docs**
5. Run tests: `pytest tests/ -v`