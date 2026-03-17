from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import AIResponse, ModerationLog, Post
from app.schemas.ai_response import AIResponseWithPost


class ModerationService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def get_pending_responses(self) -> List[AIResponseWithPost]:
        responses = (
            self.db.query(AIResponse)
            .filter(AIResponse.status == "pending")
            .order_by(AIResponse.created_at.desc)
            .all()
        )
        return [self._with_post(r) for r in responses]

    def approve(self, response_id: int, reviewer: Optional[str] = None) -> AIResponse:
        response = (
            self.db.query(AIResponse)
            .filter(AIResponse.id == response_id)
            .first()
        )
        if not response:
            raise ValueError(f"Response {response_id} not found")

        if response.status != "pending":
            raise ValueError(f"Response is not pending (status: {response.status})")

        response.status = "approved"
        response.approved_at = datetime.utcnow()

        log = ModerationLog(
            response_id=response_id,
            action="approved",
            reviewer=reviewer,
        )
        self.db.add(log)
        self.db.commit()
        return response

    def reject(
        self, response_id: int, reason: str, reviewer: Optional[str] = None
    ) -> AIResponse:
        response = (
            self.db.query(AIResponse)
            .filter(AIResponse.id == response_id)
            .first()
        )
        if not response:
            raise ValueError(f"Response {response_id} not found")

        response.status = "rejected"
        response.rejection_reason = reason

        log = ModerationLog(
            response_id=response_id,
            action="rejected",
            reviewer=reviewer,
            feedback=reason,
        )
        self.db.add(log)
        self.db.commit()
        return response

    def _with_post(self, response: AIResponse) -> dict:
        return {
            "id": response.id,
            "post_id": response.post_id,
            "response_text": response.response_text,
            "quality_score": response.quality_score,
            "status": response.status,
            "created_at": response.created_at,
            "post": {
                "id": response.post.id,
                "skool_post_id": response.post.skool_post_id,
                "title": response.post.title,
                "content": response.post.content,
                "category": response.post.category,
                "author": response.post.author,
            },
        }
