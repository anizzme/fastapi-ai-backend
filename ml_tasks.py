import time
from celery import Celery

# 1. Initialize the Celery Worker Team
# The 'broker' is the Redis server (where FastAPI drops the basket)
# The 'backend' is also Redis (where Celery leaves the final ML result)
celery_app = Celery(
    "ml_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# 2. The Heavy ML Task (This runs completely separate from FastAPI)
@celery_app.task
def process_inference_task(image_name: str):
    print(f"\n[CELERY WORKER] PICKED UP TASK: Loading PyTorch CNN for {image_name}...")
    
    # Simulating the heavy 5-second processing time
    time.sleep(5) 
    
    print(f"[CELERY WORKER] FINISHED TASK: Prediction complete for {image_name}.\n")
    return "Defect Detected (94.8% confidence)"