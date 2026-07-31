from fastapi import FastAPI
from database import engine
from models import Base

# Import BOTH of your routers now
from routers import users
from routers import predict 

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routes from our modular files
app.include_router(users.router)
app.include_router(predict.router) # Injecting the new ML route!

@app.get("/")
def read_root():
    return {"message": "Enterprise Architecture is Online!"}