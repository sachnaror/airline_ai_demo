# Airline AI Demo (FastAPI + LangChain + LangGraph + LangFlow + Postgres)

End‑to‑end demo where you can ask natural language questions about ONE airline's booking data.
Includes:
- FastAPI service layer
- Postgres with 500 demo bookings
- Three paths: LangChain / LangGraph / LangFlow
- OpenAI LLM for reasoning

## 1) Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your OpenAI key and Postgres URL
```

Create the database (example for local Postgres):
```bash
createdb airline_demo  # or use psql to create the DB
```

## 2) Load demo data (500 rows)
```bash
python -m app.ingest_data
```

## 3) Run API
```bash
uvicorn app.main:app --reload --port 8000
```

## 4) Try queries
```bash
# Compare all three engines at once
curl "http://127.0.0.1:8000/ask?query=Which flight is most in demand?"

# Specific helpers
curl "http://127.0.0.1:8000/analytics/top-day"
curl "http://127.0.0.1:8000/analytics/top-hour"
curl "http://127.0.0.1:8000/analytics/top-flight"
```

## Notes
- Replace the dummy search logic with warehouse queries as needed.
- LangFlow is included as a stub; export a flow JSON from LangFlow and wire it in `app/services/langflow_service.py` where indicated.
- Safe NL→SQL is non‑trivial; start with controlled templates or a whitelist of metrics/dimensions.


## 📩 Contact

| Name              | Details                             |
|-------------------|-------------------------------------|
| **👨‍💻 Developer**  | Sachin Arora                      |
| **📧 Email**      | [sachnaror@gmail.com](mailto:sacinaror@gmail.com) |
| **📍 Location**   | Noida, India                       |
| **📂 GitHub**     | [Github.com/sachnaror](https://github.com/sachnaror) |
| **🌐 Youtube**    | [My_Youtube](https://www.youtube.com/@sachnaror4841/videos) |
| **🌐 Blog**       | [My_Blog](https://medium.com/@schnaror) |
| **🌐 Website**    | [About_Me](https://about.me/sachin-arora) |
| **🌐 Twitter**    | [Twitter](https://twitter.com/sachinhep) |
| **📱 Phone**      | [+91 9560330483](tel:+919560330483) |
