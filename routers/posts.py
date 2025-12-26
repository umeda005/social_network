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

@router.put("/{post_id}")
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db)
):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    if post.content is not None:
        db_post.content = post.content

    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Пост не найден")

    db.delete(db_post)
    db.commit()

    return {"detail": "Пост удалён"}

