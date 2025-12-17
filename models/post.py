from pydantic import BaseModel, Field

class Post(BaseModel):
    author_id: int = Field(..., example=1)
    content: str = Field(..., example="Новый пост")
