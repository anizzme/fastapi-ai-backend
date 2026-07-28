# Scalable ML Inference API (Backend Engine)

## Overview

This repository contains a robust, asynchronous REST API architected to serve as the backend data layer for Machine Learning inference models. Built with **FastAPI** and **PostgreSQL**, this system is designed for low-latency data processing, secure environment configuration, and strict payload validation.

## Architecture & Tech Stack

* **Framework:** FastAPI (Python 3.x)
* **Database:** PostgreSQL (Relational Data Persistence)
* **ORM:** SQLAlchemy V2.0
* **Data Validation:** Pydantic
* **Security:** python-dotenv (Environment Variable Management)

## Key Engineering Features

* **Asynchronous Routing:** Non-blocking endpoints prepared for high-throughput AI inference requests.
* **ACID-Compliant Transactions:** Ensures data integrity during concurrent database writes via SQLAlchemy.
* **Strict Schema Validation:** Pydantic models automatically sanitize and validate incoming JSON payloads, preventing malformed data from crashing the server.
* **Enterprise Security:** Environment variables (`.env`) utilized to completely isolate and secure database credentials from the codebase.

## Local Setup Instructions

1. Clone the repository: `git clone https://github.com/anizzme/fastapi-ai-backend.git`
2. Install dependencies: `pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv`
3. Create a `.env` file in the root directory and add your local PostgreSQL connection string:
   `DATABASE_URL=postgresql://username:password@localhost/ai_backend`
4. Start the Uvicorn ASGI server: `uvicorn main:app --reload`
5. Access the interactive API documentation (Swagger UI) at: `http://127.0.0.1:8000/docs`