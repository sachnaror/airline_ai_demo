from pydantic import BaseModel
from sqlalchemy import text
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from ..config import OPENAI_API_KEY
from ..db import SessionLocal

def _llm():
    if not OPENAI_API_KEY:
        return None
    return ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

class State(BaseModel):
    query: str
    context: str = ""
    answer: str = ""

def fetch_context(state: State):
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

    state.context = f"Highest bookings day: {top_day.day} ({top_day.cnt}).\n" \                    f"Busiest booking hour: {int(top_hour.hour)}:00 ({top_hour.cnt}).\n" \                    f"Most in-demand flight: {top_flight.flight_number} ({top_flight.cnt})."
    return state

def answer_with_llm(state: State):
    model = _llm()
    if model is None:
        state.answer = state.context  # fallback if no key
        return state
    prompt = f"User question: {state.query}\nContext:\n{state.context}\nReturn a concise answer."
    resp = model.invoke(prompt)
    state.answer = resp.content
    return state

# Build workflow
workflow = StateGraph(State)
workflow.add_node("fetch_context", fetch_context)
workflow.add_node("answer_with_llm", answer_with_llm)
workflow.set_entry_point("fetch_context")
workflow.add_edge("fetch_context", "answer_with_llm")
workflow.add_edge("answer_with_llm", END)
graph = workflow.compile()

def langgraph_query(user_query: str):
    final = graph.invoke(State(query=user_query))
    return {"method": "LangGraph", "answer": final.answer}
