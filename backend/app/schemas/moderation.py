from datetime import datetime
from typing import Optional
from pydantic import BaseModel


from app.schemas.post import PostResponse


class ModerationAction(Base):
    action: str
    reviewer: Optional[str] = None
    feedback: Optional[str] = None


class ModerationLogResponse(Base):
    id: int
    response_id: int
    action: str
    reviewer: Optional[str] = None
    feedback: Optional[str] = None
    created_at: datetime
