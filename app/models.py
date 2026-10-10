import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    task: Mapped[str] = mapped_column(String(50), index=True)
    input_text: Mapped[str] = mapped_column(Text)
    label: Mapped[str] = mapped_column(String(50))
    confidence: Mapped[float] = mapped_column(Float)
    inference_ms: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, index=True
    )