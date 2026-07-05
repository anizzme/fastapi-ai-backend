from fastapi import FastAPI

# This creates your actual web server app
app = FastAPI()

# This tells the server: "If someone visits the home page (/), run this function."
@app.get("/")
def read_root():
    return {"message": "My AI Backend is Alive!"}
