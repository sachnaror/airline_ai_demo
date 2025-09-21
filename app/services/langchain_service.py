from sqlalchemy import text
from langchain_openai import ChatOpenAI
from ..utils.prompts import BOOKING_PROMPT
from ..config import OPENAI_API_KEY
from ..db import SessionLocal

def _llm():
    if not OPENAI_API_KEY:
        return None
    return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

def langchain_query(user_query: str):
    # Simple analytics: find day with highest bookings
    with SessionLocal() as db:
        top_day = db.execute(text("""
            SELECT DATE(booking_time) as day, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()

        top_hour = db.execute(text("""
            SELECT EXTRACT(HOUR FROM booking_time)::int as hour, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()

        top_flight = db.execute(text("""
            SELECT flight_number, COUNT(*) as cnt
            FROM flight_bookings
            GROUP BY 1
            ORDER BY cnt DESC
            LIMIT 1;
        """)).fetchone()

    context = f"Highest bookings day: {top_day.day} ({top_day.cnt}).\n" \              f"Busiest booking hour: {int(top_hour.hour)}:00 ({top_hour.cnt}).\n" \              f"Most in-demand flight: {top_flight.flight_number} ({top_flight.cnt})."

    model = _llm()
    if model is None:
        # No LLM key set; return fallback
        return {"method": "LangChain", "answer": context, "llm": "disabled"}

    resp = model.invoke(BOOKING_PROMPT.format(query=user_query, context=context))
    return {"method": "LangChain", "answer": resp.content}
