from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Post, Job


class ScraperHandler:
    def __init__(self, db: Session):
        self.db = db

    def ingest_post(self, post_data: dict) -> Post:
        existing = (
            self.db.query(Post)
            .filter(Post.skool_post_id == post_data["skool_post_id"])
            .first()
        )

        if existing:
            existing.reply_count = post_data.get("reply_count", existing.reply_count)
            existing.likes = post_data.get("likes", existing.likes)
            self.db.commit()
            return existing

        post = Post(
            skool_post_id=post_data["skool_post_id"],
            title=post_data.get("title"),
            content=post_data.get("content"),
            category=post_data.get("category"),
            author=post_data.get("author"),
            post_url=post_data.get("post_url"),
            reply_count=post_data.get("reply_count", 0),
            likes=post_data.get("likes", 0),
            created_at=post_data.get("created_at"),
        )
        self.db.add(post)
        self.db.commit()
        return post

    def ingest_batch(self, posts: List[dict]) -> List[Post]:
        return [self.ingest_post(post) for post in posts]

    def should_process(self, post: Post) -> bool:
        settings = get_settings()
        
        if post.reply_count > 0:
            return False

        if post.processed:
            return False

        if post.created_at:
            age_hours = (datetime.utcnow() - post.created_at).total_seconds / 3600
            if age_hours > settings.POST_MAX_AGE_HOURS:
                return False

        return True

    def create_job(self, post: Post) -> Job:
        job = Job(
            post_id=post.id,
            job_type="generate_reply",
            status="pending",
        )
        self.db.add(job)
        self.db.commit()
        return job
