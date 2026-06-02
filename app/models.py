from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, func
from sqlalchemy import DateTime
from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    content: Mapped[str] = mapped_column(String(200),nullable=False)
    published: Mapped[bool] = mapped_column(server_default="FALSE")
    votes: Mapped[int] = mapped_column(default=0)

    created_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_ts: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False) 
    
    created_ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_ts: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete")


class Vote(Base):
    __tablename__ = "votes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
