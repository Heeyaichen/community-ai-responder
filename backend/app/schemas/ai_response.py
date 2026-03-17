from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class AIResponseBase(Base):
    model_config = ConfigDict(protected=True)


class AIResponseCreate(AIResponseBase):
    post_id: int
    response_text: str
    model_used: Optional[str] = None
    prompt_version: Optional[str] = None
    quality_score: Optional[float] = None


class AIResponseUpdate(AIResponseBase):
    status: Optional[str] = None
    quality_score: Optional[float] = None
    rejection_reason: Optional[str] = None


class AIResponseResponse(AIResponseBase):
    id: int
    created_at: datetime
    status: str
    approved_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AIResponseWithPost(AIResponseResponse):
    post: "PostResponse"


class PendingResponseList(Base):
    responses: List[AIResponseWithPost]
    total: int
