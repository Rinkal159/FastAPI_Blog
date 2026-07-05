from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from env_config import settings
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI

engine = create_async_engine(settings.postgres_url)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(), unique=True)
    password: Mapped[str] = mapped_column(String())
    profile_picture: Mapped[str] = mapped_column(String(), nullable=True)
    bio: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    blogs: Mapped[list["Blog"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    
    @property
    def profile_picture_path(self):
        if self.profile_picture:
            return f"media/profic_pictures/{self.profile_picture}"
        return "static/profile_pictures/default.jpg"


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(1500))
    posted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    author: Mapped["User"] = relationship(back_populates="blogs", lazy="selectin")



# asynchronous way to create database tables
@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    
