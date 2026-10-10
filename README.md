# Distributed AI Inference API

![CI](https://github.com/anizzme/fastapi-ai-backend/actions/workflows/ci.yml/badge.svg)

An asynchronous REST API that validates, routes and persists ML inference requests.
Built with FastAPI, PostgreSQL, SQLAlchemy 2.0 (async) and Pydantic v2.

## Features

- **Async end to end:** FastAPI + `asyncpg` driver; model code runs in a thread pool so the event loop is never blocked.
- **Strict validation:** Pydantic v2 rejects malformed payloads with HTTP 422 before they reach the model or database.
- **Task routing:** a model registry routes each request (`sentiment`, `toxicity`) to the right model. New models plug in without touching the API.
- **ACID persistence:** every prediction is saved in a PostgreSQL transaction with rollback on failure.
- **Observability:** `X-Process-Time-Ms` header on every response and a `/health` endpoint that checks the database.
- **Tested and containerised:** pytest suite (incl. a 200-request concurrency test), Docker Compose, GitHub Actions CI.

## Architecture

```
Client -> FastAPI (validate -> route -> run model) -> SQLAlchemy async session -> PostgreSQL
```

## Run it

```bash
docker compose up --build
```

Open http://localhost:8000/docs for interactive Swagger docs.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/v1/predict` | Run inference and store the result |
| GET | `/api/v1/predictions/{id}` | Fetch one stored prediction |
| GET | `/api/v1/predictions?limit=20&offset=0` | List predictions (paginated) |
| GET | `/health` | Liveness + database check |

Example:

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"task": "sentiment", "text": "I love this product"}'
```

## Performance (measured with Locust)

Test machine: FILL IN (CPU, RAM, OS). Server: 4 Uvicorn workers via Docker Compose.

| Concurrent users | Requests/sec | p50 latency | p95 latency | p99 latency | Failures |
| --- | --- | --- | --- | --- | --- |
| 500 | FILL | FILL | FILL | FILL | FILL |
| 5,000 | FILL | FILL | FILL | FILL | FILL |

## Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Roadmap

Alembic migrations, real ML models (scikit-learn / ONNX), authentication, Prometheus metrics.