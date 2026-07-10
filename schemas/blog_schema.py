from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime


class Base(BaseModel):
    pass


class BlogCreate(Base):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    content: Annotated[str, Field(min_length=10, max_length=1500)]
    

class BlogUpdate(Base):
    title: str | None = None
    content: str | None = None


class AuthorDetail(Base):
    name: str
    profile_picture: str | None
    profile_picture_path: str
    bio: str | None
    
    model_config = ConfigDict(from_attributes=True)


# inheritated from BlogCreate
class BlogResponse(BlogCreate):
    posted_at: datetime
    updated_at: datetime
    author: AuthorDetail
    
    model_config = ConfigDict(from_attributes=True)
        
        
class PaginatedBlogResponse(Base):
    blogs: list[BlogResponse]
    page: int
    skip: int
    limit: int
    has_more: bool
