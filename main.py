from fastapi import FastAPI
from pydantic import BaseModel

# This creates your actual web server app
app = FastAPI()

#Create a Pydantic blueprint. This tells FastAPI what incoming data should look like
class UserInput(BaseModel):
    name: str
    age: int

# This tells the server: "If someone visits the home page (/), run this function."
# existing get route
@app.get("/")
def read_root():
    return {"message": "My AI Backend is Alive!"}

#new post route
@app.post("/submit")
def submit_data(data: UserInput):
    #we take the data we received and send a custom message back
    return{
        "status": "Success",
        "message": f"Hello {UserInput.name}, I see you are {UserInput.age} years old!"
    }
