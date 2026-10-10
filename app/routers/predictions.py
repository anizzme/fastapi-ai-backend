from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import PredictionResponse, PredictRequest
from app.services.inference import run_inference

router = APIRouter(prefix="/api/v1", tags=["predictions"])


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_prediction(payload: PredictRequest, db: AsyncSession = Depends(get_db)):
    # 1) payload already validated by Pydantic
    # 2) route to the right model and run it (no DB connection held yet)
    result = await run_inference(payload.task, payload.text)
    # 3) persist in one ACID transaction
    return await crud.create_prediction(db, payload.task, payload.text, result)


@router.get("/predictions/{prediction_id}", response_model=PredictionResponse)
async def read_prediction(prediction_id: UUID, db: AsyncSession = Depends(get_db)):
    record = await crud.get_prediction(db, prediction_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return record


@router.get("/predictions", response_model=list[PredictionResponse])
async def read_predictions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_predictions(db, limit, offset)