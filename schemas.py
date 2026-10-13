from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PredictRequest(BaseModel):
    task: Literal["sentiment", "toxicity"]
    text: str = Field(min_length=1, max_length=1000)

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must not be blank")
        return value


class PredictResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task: str
    text: str
    label: str
    confidence: float
    created_at: datetime