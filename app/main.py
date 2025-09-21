from fastapi import FastAPI, Query
from sqlalchemy import text
from .db import SessionLocal, init_db
from .services.langchain_service import langchain_query
from .services.langgraph_service import langgraph_query
from .services.langflow_service import langflow_query

app = FastAPI(title="Airline AI Demo")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ask")
def ask(query: str = Query(..., description="Natural language question about bookings")):
    lc = langchain_query(query)
    lg = langgraph_query(query)
    lf = langflow_query(query)
    return {"LangChain": lc, "LangGraph": lg, "LangFlow": lf}

@app.get("/analytics/top-day")
def top_day():
    with SessionLocal() as db:
        row = db.execute(text("""
            SELECT DATE(booking_time) as day, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()
    return {"day": str(row.day), "bookings": row.cnt}

@app.get("/analytics/top-hour")
def top_hour():
    with SessionLocal() as db:
        row = db.execute(text("""
            SELECT EXTRACT(HOUR FROM booking_time)::int as hour, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()
    return {"hour": int(row.hour), "bookings": row.cnt}

@app.get("/analytics/top-flight")
def top_flight():
    with SessionLocal() as db:
        row = db.execute(text("""
            SELECT flight_number, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()
    return {"flight_number": row.flight_number, "bookings": row.cnt}
