from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Prediction
from app.schemas import TaskType
from app.services.inference import InferenceResult


async def create_prediction(
    db: AsyncSession, task: TaskType, text: str, result: InferenceResult
) -> Prediction:
    record = Prediction(
        task=task.value,
        input_text=text,
        label=result.label,
        confidence=result.confidence,
        inference_ms=result.inference_ms,
    )
    db.add(record)
    try:
        await db.commit()  # ACID: all-or-nothing
    except SQLAlchemyError:
        await db.rollback()  # undo everything if anything failed
        raise
    await db.refresh(record)
    return record


async def get_prediction(db: AsyncSession, prediction_id: UUID) -> Prediction | None:
    return await db.get(Prediction, prediction_id)


async def list_predictions(db: AsyncSession, limit: int, offset: int) -> list[Prediction]:
    stmt = (
        select(Prediction)
        .order_by(Prediction.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.scalars(stmt)
    return list(result.all())