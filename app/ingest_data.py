import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .db import FlightBooking, init_db, SessionLocal

# Generate 500 demo rows for a single airline (e.g., 'SB' - SkyBlue Airways)
def generate_records(n=500):
    records = []
    base_date = datetime(2025, 8, 1, 0, 0, 0)
    airline_code = "SB"  # single airline code
    # 20 flights (same airline) serving a few Indian routes
    routes = [
        ("Delhi", "Mumbai"),
        ("Delhi", "Bangalore"),
        ("Delhi", "Dubai"),
        ("Mumbai", "Goa"),
        ("Bangalore", "Delhi"),
        ("Mumbai", "Delhi"),
    ]
    flight_nums = [f"{airline_code}{100 + i}" for i in range(20)]

    # Make some flights naturally more popular to create interesting analytics
    popularity_boost = {flight_nums[i]: (3 if i % 5 == 0 else 1) for i in range(len(flight_nums))}

    for i in range(n):
        flight_number = random.choices(flight_nums, weights=[popularity_boost[f] for f in flight_nums])[0]
        origin, destination = random.choice(routes)
        # Spread bookings across the month and hours
        booking_time = base_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        passenger_name = f"Passenger_{i+1:04d}"
        records.append(dict(
            flight_number=flight_number,
            origin=origin,
            destination=destination,
            booking_time=booking_time,
            passenger_name=passenger_name
        ))
    return records

def load_data(n=500):
    init_db()
    db: Session = SessionLocal()
    try:
        for row in generate_records(n):
            db.add(FlightBooking(**row))
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    load_data()
    print("✅ Loaded 500 demo booking rows into Postgres.")
