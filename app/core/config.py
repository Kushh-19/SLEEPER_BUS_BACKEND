MEAL_PRICE = 100

STATIONS = {
    "Ahmedabad": 1,
    "Vadodara": 2,
    "Surat": 3,
    "Mumbai": 4,
}

# Route is "Long" (high demand) only for full Ahmedabad -> Mumbai
LONG_ROUTE_SOURCE = "Ahmedabad"
LONG_ROUTE_DESTINATION = "Mumbai"

SEATS = [
    {"id": "L1", "category": "lower", "price": 700},
    {"id": "L2", "category": "lower", "price": 700},
    {"id": "L3", "category": "lower", "price": 700},
    {"id": "U1", "category": "upper", "price": 500},
    {"id": "U2", "category": "upper", "price": 500},
    {"id": "U3", "category": "upper", "price": 500},
]

SEAT_IDS = [s["id"] for s in SEATS]
