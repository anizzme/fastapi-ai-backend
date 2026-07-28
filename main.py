from fastapi import FastAPI
from database import engine
from models import Base
from routers import users

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routes from our modular file
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Enterprise Architecture is Online!"}