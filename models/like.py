from pydantic import BaseModel, Field

class Like(BaseModel):
    user_id: int = Field(..., example=1)
    post_id: int = Field(..., example=2)
