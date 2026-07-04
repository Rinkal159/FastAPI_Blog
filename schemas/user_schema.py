from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from datetime import datetime


class Base(BaseModel):
    pass


class UserCreate(Base):
    name: Annotated[str, Field(min_length=4, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    bio: Annotated[str | None, Field(max_length=1500)] = None
    profile_picture: str | None = None
    
    
class UserUpdate(Base):
    name: str | None = None
    bio: str | None = None
    profile_picture: str | None = None


# inherited from UserCreate
class UserResponse(Base):
    name: str
    email: str
    bio: str | None
    profile_picture: str | None
    profile_picture_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
