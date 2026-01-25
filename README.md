# Sleeper Bus Booking System (Ahmedabad → Mumbai)

## 📌 Project Overview
[cite_start]This project is a web-based booking system designed for a single sleeper bus service operating between Ahmedabad and Mumbai[cite: 7, 10]. [cite_start]The system features an interactive seat selection flow, a unique meal integration service, and an AI-powered Waitlist Prediction engine to estimate confirmation chances for waitlisted tickets[cite: 8, 36].

**Role:** AI/ML Software Engineer  
**Timeline:** Jan 2026

---

## 🎨 UI/UX Prototype
**[PASTE YOUR FIGMA / ADOBE XD LINK HERE]**
> [cite_start]*Note: This prototype demonstrates the visual flow from search to booking confirmation.* [cite: 24]

---

## 🚀 Core Features (Web Flow)
[cite_start]*Per assignment requirements, here are the defined core features:* [cite: 15]

### 1. Smart Route & Seat Visualization
* [cite_start]Users can select source and destination (including intermediate stops like Vadodara/Surat)[cite: 11].
* The system dynamically filters seat availability based on the specific route segment to maximize occupancy (e.g., a seat booked from Ahmedabad to Vadodara is shown as "Available" for a Vadodara to Mumbai search).

### 2. Interactive Deck Layout (Sleeper/Seater)
* Visual representation of the bus layout, distinguishing between **Lower Deck** (Seater/Sleeper mix) and **Upper Deck** (Sleeper only).
* Clear color-coding for status: *Available (Green), Booked (Grey), Selected (Blue).*

### 3. Integrated Meal Booking Service (Unique Feature)
* [cite_start]During the checkout process, users can add meal packs (Veg/Non-Veg) directly to their ticket[cite: 8].
* The system calculates the total fare (Seat Price + Meal Cost) in real-time before payment.

### 4. AI-Powered Confirmation Prediction
* [cite_start]For waitlisted seats, the system displays a **"Confirmation Probability %"**[cite: 36].
* This is calculated using a custom prediction engine that analyzes Queue Position, Days to Departure, and Historical Route Demand.

### 5. Real-Time Conflict Detection
* Prevents "Double Booking" errors. If two users try to book the same seat simultaneously, the system locks the seat for the first request and alerts the second user immediately.

### 6. Seamless Cancellation & Refund Calculation
* [cite_start]Users can cancel their booking via a simple PNR lookup[cite: 33].
* The system automatically calculates the refundable amount based on the cancellation policy logic implemented in the backend.

---

## 🧪 Critical Test Cases
[cite_start]*Comprehensive QA plan covering Functional, Edge, and UI scenarios.* [cite: 17]

### [cite_start]A. Functional Test Cases [cite: 18]
1.  **Verify Route Logic:** Searching for "Vadodara to Ahmedabad" (Reverse/Invalid direction) should show an error or 0 buses.
2.  **Verify Price Calculation:** Select 1 Seat (700) + 2 Meals (200). Total should exactly equal 900.
3.  **Verify Booking Persistence:** After a successful booking, the seat must appear "Booked" for subsequent users searching the same segment.
4.  **Verify Cancellation:** Canceling a booking should immediately free up the seat for new users.

### [cite_start]B. Edge Cases [cite: 19]
1.  **Segment Overlap:** If Seat L1 is booked *Ahmedabad -> Vadodara*, a new user **MUST** be able to book Seat L1 for *Vadodara -> Mumbai*.
2.  **The "Last Minute" Prediction:** A user checking prediction for a waitlist seat < 2 hours before departure should receive a very low (<5%) probability score.
3.  **Concurrency:** Two API requests hitting `/book` for the same seat at the exact same millisecond. (Handled via backend status checks).
4.  **Negative Meals:** Attempting to order "-1" meals in the API payload should return a Validation Error (422 Unprocessable Entity).

### [cite_start]C. UI/UX Validation Cases [cite: 20]
1.  **Mobile Responsiveness:** The bus seat layout must scroll horizontally or stack correctly on mobile screens.
2.  **Loading States:** When the AI Prediction is calculating, a skeleton loader or spinner must be shown to prevent user drop-off.
3.  **Error Feedback:** If a payment fails or a seat is taken, the error message must be human-readable (e.g., *"Sorry, this seat was just booked!"*) rather than a raw 500 server error.

---

## 🛠️ Tech Stack & Setup
* [cite_start]**Backend:** Python (FastAPI) [cite: 27]
* **Data Validation:** Pydantic
* [cite_start]**Prediction Logic:** Custom Heuristic Engine (Simulated Logistic Regression) [cite: 37]

### How to Run
1.  **Install Dependencies:**
    ```bash
    pip install fastapi uvicorn
    ```
2.  **Start Server:**
    ```bash
    uvicorn main:app --reload
    ```
3.  **Access API Docs:**
    Open `http://127.0.0.1:8000/docs` to test endpoints.

---