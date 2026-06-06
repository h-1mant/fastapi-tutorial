from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr

class PostCreate(BaseModel):
    title: str = Field(description="Post Title", max_length=50)
    content: str = Field(description="Post Content", max_length=200)
    published: bool = Field(description="Post Publication Status", default=False)
    user_id: Optional[int] = None

    model_config = {"from_attributes": True, "extra": "forbid"}

class PostUpdate(PostCreate):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(PostCreate):
    id: int = Field(description="Post ID")
    votes: int = Field(description="Post Upvotes")
    created_ts: datetime = Field(description="Post Creation Timestamp")
    updated_ts: Optional[datetime] = Field(description="Post Last Updated Timestamp", default=None) # pyright: ignore[reportUndefinedVariable]


class UserCreate(BaseModel):
    email: EmailStr 
    password: str

    model_config = {"extra": "forbid"}

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_ts: datetime
    updated_ts: Optional[datetime]

    model_config = {"extra": "forbid"}

class UserLogin(UserCreate):
    pass

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str

    model_config = {"extra": "forbid"}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

    model_config = {"extra": "forbid"}

class VoteCreate(BaseModel):
    post_id: int
    vote_dir: Literal[0,1]

    model_config = {"extra": "forbid"}
    
class VoteResponse(VoteCreate):
    pass