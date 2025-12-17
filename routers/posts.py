from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.post import Post
from models_db.post_db import PostDB

router = APIRouter(prefix="/posts", tags=["Posts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostDB).all()

@router.post("/")
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = PostDB(
        author_id=post.author_id,
        content=post.content,
        likes=0
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
