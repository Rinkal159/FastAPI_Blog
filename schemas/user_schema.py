from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from datetime import datetime
from fastapi import Form


class Base(BaseModel):
    pass


class UserCreate(Base):
    name: Annotated[str, Field(min_length=4, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    bio: Annotated[str | None, Field(max_length=1500)] = None
    
    @classmethod
    def as_form(
        cls, 
        name: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...),
        bio: str | None = Form(None),
    ):
        return cls(
            name=name,
            email=email,
            password=password,
            bio=bio
        )
    
    
    
class UserUpdate(Base):
    name: str | None = None
    bio: str | None = None
    
    @classmethod
    def as_form(
        cls, 
        name: str | None = Form(None),
        bio: str | None = Form(None)
    ):
        return cls(
            name=name,
            bio=bio
        )


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
        
        
class UserPassword(Base):
    current_password: str
    new_password: Annotated[str, Field(
        min_length=8
    )]
