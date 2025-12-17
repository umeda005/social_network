#логика хэширования и проверки
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models_db.user_db import UserDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
