from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import DBUser
from schemas import UserInput

router = APIRouter()

@router.post("/submit")
def submit_data(data: UserInput, db: Session = Depends(get_db)):
    new_user = DBUser(name=data.name, age=data.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "Success", "message": f"Saved {data.name} with ID {new_user.id}"}

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(DBUser).all()
    return {"database_records": users}