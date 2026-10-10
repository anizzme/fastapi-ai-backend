import re
import time
from dataclasses import dataclass
from typing import Protocol

from fastapi.concurrency import run_in_threadpool

from app.schemas import TaskType


class InferenceModel(Protocol):
    def predict(self, text: str) -> tuple[str, float]: ...


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


class SentimentModel:
    POSITIVE = frozenset(
        {"love", "great", "good", "excellent", "amazing", "happy",
         "fantastic", "wonderful", "best", "awesome"}
    )
    NEGATIVE = frozenset(
        {"hate", "terrible", "bad", "awful", "worst", "horrible",
         "poor", "sad", "disappointing", "boring"}
    )

    def predict(self, text: str) -> tuple[str, float]:
        tokens = _tokenize(text)
        pos = sum(t in self.POSITIVE for t in tokens)
        neg = sum(t in self.NEGATIVE for t in tokens)
        if pos > neg:
            return "positive", round(pos / (pos + neg), 4)
        if neg > pos:
            return "negative", round(neg / (pos + neg), 4)
        return "neutral", 0.5


class ToxicityModel:
    TOXIC_WORDS = frozenset({"idiot", "stupid", "moron", "dumb", "loser", "trash", "hate"})

    def predict(self, text: str) -> tuple[str, float]:
        hits = sum(t in self.TOXIC_WORDS for t in _tokenize(text))
        if hits == 0:
            return "non_toxic", 0.9
        return "toxic", round(min(0.99, 0.6 + 0.15 * hits), 2)


# The router: task name -> model that handles it.
MODEL_REGISTRY: dict[TaskType, InferenceModel] = {
    TaskType.SENTIMENT: SentimentModel(),
    TaskType.TOXICITY: ToxicityModel(),
}


@dataclass(frozen=True)
class InferenceResult:
    label: str
    confidence: float
    inference_ms: float


async def run_inference(task: TaskType, text: str) -> InferenceResult:
    model = MODEL_REGISTRY[task]
    start = time.perf_counter()
    # Model code is CPU work. Running it in a thread keeps the event loop free.
    label, confidence = await run_in_threadpool(model.predict, text)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return InferenceResult(label, confidence, round(elapsed_ms, 3))