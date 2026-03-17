from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import AIResponse
from app.schemas.ai_response import AIResponseResponse, AIResponseWithPost
from app.services.moderation_service import ModerationService
from app.schemas.moderation import ModerationAction


router = APIRouter(prefix="/responses", tags=["moderation"])


class ApproveRequest(BaseModel):
    reviewer: str | None = None


class RejectRequest(BaseModel):
    reason: str
    reviewer: str | None = None


@router.get("/pending", response_model=dict)
def get_pending_responses(
    db: Session = Depends(get_db)
):
    service = ModerationService(db)
    responses = service.get_pending_responses()
    return {"responses": responses, "total": len(responses)}


@router.post("/{response_id}/approve", response_model=AIResponseResponse)
def approve_response(
    response_id: int,
    request: ApproveRequest,
    db: Session = Depends(get_db)
):
    service = ModerationService(db)
    try:
        response = service.approve(response_id, request.reviewer)
        return AIResponseResponse.model_validate(response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{response_id}/reject", response_model=AIResponseResponse)
def reject_response(
    response_id: int,
    request: RejectRequest,
    db: Session = Depends(get_db)
):
    service = ModerationService(db)
    try:
        response = service.reject(response_id, request.reason, request.reviewer)
        return AIResponseResponse.model_validate(response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{response_id}", response_model=AIResponseWithPost)
def get_response(
    response_id: int,
    db: Session = Depends(get_db)
):
    response = db.query(AIResponse).filter(AIResponse.id == response_id).first()
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    
    return AIResponseWithPost(
        id=response.id,
        post_id=response.post_id,
        response_text=response.response_text,
        quality_score=response.quality_score,
        status=response.status,
        created_at=response.created_at,
        post={
            "id": response.post.id,
            "skool_post_id": response.post.skool_post_id,
            "title": response.post.title,
            "content": response.post.content,
            "category": response.post.category,
            "author": response.post.author,
        }
    )
