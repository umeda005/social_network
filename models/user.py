from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., example="new_user")
