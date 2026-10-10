import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app import models  # noqa: F401
from app.database import engine
from app.routers import health, predictions

logger = logging.getLogger("ai_backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()  # close DB connections on shutdown


app = FastAPI(
    title="Distributed AI Inference API",
    description="Async FastAPI service that validates, routes and persists ML inference requests.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-Ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
    return response


@app.exception_handler(SQLAlchemyError)
async def database_error_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("Database error")
    return JSONResponse(status_code=503, content={"detail": "Database temporarily unavailable"})


app.include_router(health.router)
app.include_router(predictions.router)