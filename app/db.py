from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class FlightBooking(Base):
    __tablename__ = "flight_bookings"
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, index=True)  # same airline, multiple routes
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    booking_time = Column(DateTime, index=True)
    passenger_name = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
