from sqlalchemy import create_engine, String, DateTime, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from .env_config import settings
from datetime import datetime

engine = create_engine(settings.postgres_url)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    profile_picture: Mapped[str] = mapped_column(String())
    bio: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    blogs: Mapped[list["Blog"]] = relationship(back_populates="author")


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(1500))
    posted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    author: Mapped["User"] = relationship(back_populates="blogs")


Base.metadata.create_all(engine)
