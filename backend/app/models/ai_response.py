from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AIResponse(Base):
    __tablename__ = "ai_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[str] = mapped_column(String(100), nullable=True)
    prompt_version: Mapped[str] = mapped_column(String(50), nullable=True)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    posted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    post: Mapped["Post"] = relationship("Post", back_populates="ai_responses")
    moderation_logs: Mapped[list["ModerationLog"]] = relationship(
        "ModerationLog", back_populates="response", cascade="all, delete-orphan"
    )
