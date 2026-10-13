from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base, engine, get_db
from inference import MODELS
from models import InferenceResult
from schemas import PredictRequest, PredictResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:  # create the table if it is missing
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="AI Inference API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "AI Inference API is running. See /docs"}

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse, status_code=201)
async def predict(payload: PredictRequest, db: AsyncSession = Depends(get_db)):
    # 1) Pydantic has already validated the payload
    # 2) route it to the right model
    label, confidence = MODELS[payload.task](payload.text)
    # 3) save the result in one transaction
    record = InferenceResult(
        task=payload.task, text=payload.text, label=label, confidence=confidence
    )
    db.add(record)
    try:
        await db.commit()
    except Exception:
        await db.rollback()  # undo everything if saving failed
        raise
    await db.refresh(record)
    return record


@app.get("/results/{result_id}", response_model=PredictResponse)
async def get_result(result_id: int, db: AsyncSession = Depends(get_db)):
    record = await db.get(InferenceResult, result_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Result not found")
    return record