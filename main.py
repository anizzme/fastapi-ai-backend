from fastapi import FastAPI, Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
# Using DeclarativeBase for Python 3.13+ compatibility
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

# ==========================================
# 1. THE FILING CABINET SETUP (SQLAlchemy)
# ==========================================
# Create a file named 'users.db' in our folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# MODERN FIX FOR PYTHON 3.13:
class Base(DeclarativeBase):
    pass

# Define what a "Folder" looks like inside the cabinet
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # Automatically gives users ID 1, 2, 3...
    name = Column(String, index=True)
    age = Column(Integer)

# Actually build the cabinet and folders!
Base.metadata.create_all(bind=engine)

# Helper function to open the cabinet, do work, and lock it back up
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# 2. THE ROBOT & SECURITY GUARD (FastAPI & Pydantic)
# ==========================================
class UserInput(BaseModel):
    name: str
    age: int

app = FastAPI()


# ==========================================
# 3. THE ROUTES (Listening and Talking)
# ==========================================

# The Mailbox (POST) - Now saves to the filing cabinet!
@app.post("/submit")
def submit_data(data: UserInput, db: Session = Depends(get_db)):
    # The clerk writes a new folder for the user
    new_user = DBUser(name=data.name, age=data.age)
    db.add(new_user)       # Put it in the cabinet
    db.commit()            # Slam the drawer shut (save permanently)
    db.refresh(new_user)   # Look at the folder to get the new ID number
    
    return {"status": "Success", "message": f"Saved {data.name} to the database with ID {new_user.id}!"}

# The Megaphone (GET) - Now reads from the filing cabinet!
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    # The clerk grabs ALL the folders in the cabinet
    users = db.query(DBUser).all()
    return {"database_records": users}

# ==========================================
# 4. DYNAMIC ROUTES (Precision Operations)
# ==========================================

# The Targeted Megaphone (GET one specific user)
@app.get("/users/{user_id}")
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    # The clerk uses the index to instantly find the folder by ID
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    
    # BOTTLENECK CHECK: What if the folder doesn't exist?
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found in the cabinet.")
        
    return {"database_record": user}

# The Shredder (DELETE a user)
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # First, the clerk must find the folder
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Cannot delete. User not found.")
        
    # The clerk destroys the folder and permanently saves the changes
    db.delete(user)
    db.commit()
    
    return {"status": "Success", "message": f"User {user_id} has been permanently deleted."}