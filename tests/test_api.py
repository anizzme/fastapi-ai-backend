import asyncio
from uuid import uuid4

import pytest

PREDICT = "/api/v1/predict"


async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200


async def test_health_checks_database(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["database"] == "up"


async def test_sentiment_positive(client):
    r = await client.post(PREDICT, json={"task": "sentiment", "text": "I love this great product"})
    assert r.status_code == 201
    body = r.json()
    assert body["label"] == "positive"
    assert body["id"]
    assert "x-process-time-ms" in r.headers


async def test_toxicity_toxic(client):
    r = await client.post(PREDICT, json={"task": "toxicity", "text": "you are a stupid idiot"})
    assert r.status_code == 201
    assert r.json()["label"] == "toxic"


@pytest.mark.parametrize(
    "payload",
    [
        {"task": "sentiment", "text": ""},
        {"task": "sentiment", "text": "    "},
        {"task": "unknown", "text": "hello"},
        {"text": "missing task"},
        {"task": "sentiment", "text": "x" * 5001},
    ],
)
async def test_invalid_payloads_rejected(client, payload):
    r = await client.post(PREDICT, json=payload)
    assert r.status_code == 422


async def test_prediction_is_persisted_and_readable(client):
    created = await client.post(PREDICT, json={"task": "sentiment", "text": "this is the worst, so bad"})
    assert created.status_code == 201
    prediction_id = created.json()["id"]

    fetched = await client.get(f"/api/v1/predictions/{prediction_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == prediction_id
    assert fetched.json()["label"] == "negative"


async def test_unknown_prediction_returns_404(client):
    r = await client.get(f"/api/v1/predictions/{uuid4()}")
    assert r.status_code == 404


async def test_list_predictions_respects_limit(client):
    await client.post(PREDICT, json={"task": "sentiment", "text": "good"})
    r = await client.get("/api/v1/predictions", params={"limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1


async def test_list_predictions_rejects_bad_limit(client):
    r = await client.get("/api/v1/predictions", params={"limit": 1000})
    assert r.status_code == 422


async def test_many_concurrent_requests_all_succeed(client):
    async def one(i: int):
        return await client.post(PREDICT, json={"task": "sentiment", "text": f"great item {i}"})

    responses = await asyncio.gather(*(one(i) for i in range(200)))
    assert all(r.status_code == 201 for r in responses)