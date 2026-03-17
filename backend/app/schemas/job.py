from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobBase(Base):
    model_config = ConfigDict(protected=True)


class JobCreate(JobBase):
    post_id: int
    job_type: str = "generate_reply"


class JobResponse(JobBase):
    id: int
    status: str
    attempts: int
    scheduled_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobUpdate(Base):
    status: Optional[str] = None
    attempts: Optional[int] = None
