from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

class UserCreate(BaseModel):

    email : EmailStr
    password: str

class UserOut(BaseModel):
    
    user_id: int
    email : EmailStr
    created_at :datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):

    email: EmailStr
    password: str


class PostBase(BaseModel):  # Pydantic schemas to validate and serialize data in FastAPI.
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class PostOut(PostBase):

    id: int
    created_at: datetime
    user_id: int

    owner: UserOut

    class Config:
        from_attributes = True #allows reading from SQLAlchemy model

    
class PostWithLikes(BaseModel):
    Post: PostOut
    Likes: int

    class Config:
        from_attributes = True #allows reading from SQLAlchemy model


class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id : Optional[str] = None

class Like(BaseModel):

    post_id: int
    
    direction: Annotated[int, Field(le=1)]
