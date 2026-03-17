from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PostBase(Base):
    model_config = ConfigDict(protected=True)


class PostCreate(PostBase):
    skool_post_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    post_url: Optional[str] = None
    reply_count: int = 0
    likes: int = 0
    created_at: Optional[datetime] = None


class PostResponse(PostBase):
    id: int
    scraped_at: datetime
    processed: bool

    class Config:
        from_attributes = True


class PostFilter(Base):
    reply_count: Optional[int] = None
    processed: Optional[bool] = None
    max_age_hours: Optional[int] = None
