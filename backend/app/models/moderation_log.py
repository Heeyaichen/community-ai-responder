from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ai_response import AIResponse
from sqlalchemy import DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    response_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ai_responses.id"), nullable=False
    )
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    reviewer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )

    response: Mapped["AIResponse"] = relationship(
        "AIResponse", back_populates="moderation_logs"
    )
