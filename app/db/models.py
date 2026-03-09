from sqlalchemy import Column, Integer, String, Date, Boolean
from app.db.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String, unique=True, index=True)
    passenger_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(String)

    seat_ids = Column(String)  # store comma-separated for now

    source = Column(String)
    destination = Column(String)
    travel_date = Column(Date)

    num_meals = Column(Integer)
    total_price = Column(Integer)

    status = Column(String)  # CONFIRMED / WAITLISTED / CANCELLED
    waitlist_position = Column(Integer, nullable=True)
