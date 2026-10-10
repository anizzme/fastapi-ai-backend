from fastapi import APIRouter, Depends
from sqlalchemy import text as sql_text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    return {"message": "Distributed AI Inference API is online"}


@router.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(sql_text("SELECT 1"))
    return {"status": "ok", "database": "up"}