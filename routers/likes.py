from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.like import Like
from models_db.like_db import LikeDB
from models_db.post_db import PostDB

router = APIRouter(prefix="/likes", tags=["Likes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def like_post(like: Like, db: Session = Depends(get_db)):
    # записываем лайк
    db_like = LikeDB(user_id=like.user_id, post_id=like.post_id)
    db.add(db_like)

    # обновляем количество лайков
    post = db.query(PostDB).filter(PostDB.id == like.post_id).first()
    if post:
        post.likes += 1

    db.commit()
    return {"message": f"Пользователь {like.user_id} лайкнул пост {like.post_id}"}
