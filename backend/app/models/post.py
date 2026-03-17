from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skool_post_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    post_url: Mapped[str] = mapped_column(Text, nullable=True)
    reply_count: Mapped[int] = mapped_column(Integer, default=0)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    ai_responses: Mapped[list["AIResponse"]] = relationship(
        "AIResponse", back_populates="post", cascade="all, delete-orphan"
    )
    jobs: Mapped[list["Job"]] = relationship(
        "Job", back_populates="post", cascade="all, delete-orphan"
    )
