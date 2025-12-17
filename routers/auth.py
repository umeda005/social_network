from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.auth import UserRegister, UserLogin
from models_db.user_db import UserDB
from services.auth import hash_password, authenticate_user
from utils.jwt import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(data: UserRegister, db: Session = Depends(get_db)):

    existing = db.query(UserDB).filter(UserDB.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = UserDB(
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "id": new_user.id}


@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(data.username, data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(UserDB).filter(UserDB.id == payload["user_id"]).first()
    return user
