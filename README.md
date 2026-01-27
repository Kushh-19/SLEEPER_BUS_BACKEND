# Sleeper Bus Booking System (Ahmedabad → Mumbai)

## Project Overview

This project is a web-based sleeper bus booking system designed for a **single sleeper bus service** operating between **Ahmedabad and Mumbai**, with intermediate stations such as **Vadodara** and **Surat**.

The system includes an **interactive seat booking flow**, an **integrated meal booking service**, and an **AI-powered waitlist confirmation prediction engine** that estimates the likelihood of booking confirmation in percentage terms.

---

## UI/UX Prototype

**Figma Prototype Link:**  
[https://www.figma.com/proto/FgrwKbxB00Raaq4S9a7Bpf/Sleeper-Bus-Booking-%E2%80%93-Prototype?node-id=3-2572&t=oFSW2MG7FBYfomUL-1&starting-point-node-id=3%3A2572]

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
- **Data Validation:** Pydantic
- **Prediction Logic:** Custom heuristic-based engine (mock AI model)

---

### API Endpoints

#### Health Check
GET /

#### List Seats
GET /seats

#### Book Seats (with Meals)
POST /book

#### Cancel Booking
POST /cancel_booking

#### Predict Booking Confirmation
POST /predict_confirmation

---

## Booking Confirmation Prediction (AI/ML – Mock Logic)

### Prediction Goal
Estimate the probability (%) that a waitlisted booking will be confirmed.

---

### Prediction Approach
- Rule-based heuristic inspired by Logistic Regression.
- Combines queue position, time to departure, and route demand.
- Adds controlled randomness to simulate real-world uncertainty.

---

### Mock Dataset
- Simulated historical dataset (~5000 records).
- Features:
  - Waitlist position
  - Days before travel
  - Route type

---

### Output
- Confirmation probability (0–99%)
- Confidence level
- Key influencing drivers

Detailed explanation is available in **PREDICTION_APPROACH.md**.

---

## System Assumptions

- Only one bus exists in the system.
- No payment gateway integration.
- No user authentication.
- Static station list.
- Prediction model is mocked and not trained.

---

##  How to Run the Project

1. Install dependencies:
   pip install fastapi uvicorn

2. Start the server:
   uvicorn main:app --reload

3. Access API docs:
   http://127.0.0.1:8000/docs