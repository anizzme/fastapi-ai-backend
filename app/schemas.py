from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskType(str, Enum):
    SENTIMENT = "sentiment"
    TOXICITY = "toxicity"


class PredictRequest(BaseModel):
    task: TaskType
    text: str = Field(min_length=1, max_length=5000, examples=["I love this product"])

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be blank")
        return value


class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task: TaskType
    input_text: str
    label: str
    confidence: float
    inference_ms: float
    created_at: datetime