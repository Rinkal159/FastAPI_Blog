from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime

class Base(BaseModel):
    pass

class BlogResponse(Base):
    id: int
    title: str
    content: str
    author: str
    posted_at: datetime