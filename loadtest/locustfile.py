import random

from locust import HttpUser, between, task

SAMPLES = [
    "I love this amazing product",
    "This is the worst service ever",
    "The delivery arrived on tuesday",
    "you are a stupid idiot",
    "What a great and wonderful day",
]


class InferenceUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(5)
    def predict(self):
        self.client.post(
            "/api/v1/predict",
            json={"task": random.choice(["sentiment", "toxicity"]), "text": random.choice(SAMPLES)},
        )

    @task(1)
    def health(self):
        self.client.get("/health")