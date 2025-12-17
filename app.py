from fastapi import FastAPI
from database import Base, engine
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.likes import router as likes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Social Network")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(likes_router)

@app.get("/")
def root():
    return {"message": "Auth system working!"}

