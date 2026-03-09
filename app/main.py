from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.database import engine
from app.db.models import Base
from app.core.config import STATIONS, MEAL_PRICE
from app.routers import booking, seats, prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Sleeper Bus Booking API",
    description="Backend for sleeper bus bookings with seat availability, pricing, and ML-based waitlist confirmation prediction.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the HTML/CSS/JS frontend from /frontend
app.mount(
    "/frontend",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)

app.include_router(booking.router)
app.include_router(seats.router)
app.include_router(prediction.router)


@app.get("/")
def root():
    return {
        "status": "active",
        "service": "Sleeper Bus Booking API",
        "docs": "/docs",
        "frontend": "/frontend",
        "stations": list(STATIONS.keys()),
        "pricing": {"meal_price": MEAL_PRICE},
    }


@app.get("/health")
def health():
    return {"status": "ok"}
