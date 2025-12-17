from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models_db.user_db import UserDB

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()

@router.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

