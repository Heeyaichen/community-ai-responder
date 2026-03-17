from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, AIResponse
from app.schemas.post import PostCreate, PostResponse
from app.services.scraper_handler import ScraperHandler


router = APIRouter(prefix="/ingest", tags=["ingestion"])


@router.post("/posts", response_model=PostResponse, status_code=201)
def ingest_post(
    post_data: PostCreate,
    db: Session = Depends(get_db)
):
    handler = ScraperHandler(db)
    post = handler.ingest_post(post_data.model_dump())
    return PostResponse.model_validate(post)


@router.post("/posts/batch", response_model=List[PostResponse], status_code=201)
def ingest_batch(
    posts: List[PostCreate],
    db: Session = Depends(get_db)
):
    handler = ScraperHandler(db)
    ingested = handler.ingest_batch([p.model_dump() for p in posts])
    return [PostResponse.model_validate(p) for p in ingested]


@router.post("/posts/{skool_post_id}/process", response_model=PostResponse)
def process_post(
    skool_post_id: str,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.skool_post_id == skool_post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    handler = ScraperHandler(db)
    
    if not handler.should_process(post):
        raise HTTPException(
            status_code=400,
            detail="Post does not meet processing criteria"
        )

    job = handler.create_job(post)
    return PostResponse.model_validate(post)
