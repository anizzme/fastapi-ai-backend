# AI Inference API

An asynchronous REST API built with FastAPI that validates, routes and stores text-inference requests in PostgreSQL.

## What it does

- Accepts text and a task name (`sentiment` or `toxicity`) at `POST /predict`
- Validates the payload with Pydantic (empty or invalid input is rejected with HTTP 422)
- Routes the text to the matching model function
- Saves each result in PostgreSQL through SQLAlchemy (async), committing in one transaction and rolling back on failure
- Returns the result, which can be fetched later at `GET /results/{id}`

The two models are simple word-based rules, so the focus is on the API and data layer. The routing table in `inference.py` makes it easy to plug in a trained model.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to try it.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/predict` | Validate, route, run and save a prediction |
| GET | `/results/{id}` | Fetch a saved result |
| GET | `/health` | Basic health check |

## Roadmap

Automated tests, Docker for the API, load testing, a trained ML model, and migrations.