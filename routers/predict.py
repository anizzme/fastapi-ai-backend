from fastapi import APIRouter
from pydantic import BaseModel

# Import our new Celery task
from ml_tasks import process_inference_task

router = APIRouter()

# 1. The Security Guard for our ML Model
class InferencePayload(BaseModel):
    image_name: str

# 2. The ML Route
@router.post("/predict")
async def run_inference(payload: InferencePayload):
    # INSTEAD of running the model here and freezing the server,
    # we throw the task into the Redis basket using .delay()
    task = process_inference_task.delay(payload.image_name)
    
    # We instantly return a message to the user!
    return {
        "status": "Processing in background",
        "task_id": task.id,
        "message": f"Your image '{payload.image_name}' has been successfully handed off to the ML workers!"
    }