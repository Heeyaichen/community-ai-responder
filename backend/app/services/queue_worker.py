import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Post, Job, AIResponse
from app.services.context_builder import ContextBuilder
from app.services.prompt_selector import PromptSelector
from app.services.llm_service import LLMService
from app.services.quality_scorer import QualityScorer


class QueueWorker:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        self.context_builder = ContextBuilder()
        self.prompt_selector = PromptSelector()
        self.llm_service = LLMService()
        self.quality_scorer = QualityScorer(threshold=self.settings.QUALITY_SCORE_THRESHOLD)
        self.running = False

    def start(self):
        self.running = True
        asyncio.create_task(self._run_loop())

    def stop(self):
        self.running = False

    async def _run_loop(self):
        while self.running:
                job = self._fetch_next_job()
                if not job:
                    await asyncio.sleep(self.settings.JOB_QUEUE_POLL_INTERVAL)
                    continue

                try:
                    self._mark_processing(job)
                    result = await self._process_job(job)
                    self._mark_done(job)
                except Exception as e:
                    self._handle_failure(job, str(e))

    def _fetch_next_job(self) -> Optional[Job]:
        return (
            self.db.query(Job)
            .filter(Job.status == "pending")
            .filter(Job.attempts < self.settings.JOB_MAX_ATTEMPTS)
            .order_by(Job.scheduled_at)
            .first()
        )

    def _mark_processing(self, job: Job):
        job.status = "processing"
        job.updated_at = datetime.utcnow()
        self.db.commit()

    def _mark_done(self, job: Job):
        job.status = "done"
        job.updated_at = datetime.utcnow()
        self.db.commit()

    def _handle_failure(self, job: Job, error: str):
        job.attempts += 1
        job.updated_at = datetime.utcnow()
        if job.attempts >= self.settings.JOB_MAX_ATTEMPTS:
            job.status = "failed"
        else:
            job.status = "pending"
        self.db.commit()

    async def _process_job(self, job: Job) -> AIResponse:
        post = self.db.query(Post).filter(Post.id == job.post_id).first()
        if not post:
            raise ValueError(f"Post {job.post_id} not found")

        context = self.context_builder.build(post)
        prompt = self.prompt_selector.select(context.category, context.content or "")
        response_text = await asyncio.to_thread(
            self.llm_service.generate
        )(prompt)
        quality_score = self.quality_scorer.score(response_text)
        response = AIResponse(
            post_id=post.id,
            response_text=response_text,
            model_used=self.settings.OPENAI_MODEL,
            prompt_version="v1",
            quality_score=quality_score,
            status="pending",
        )
        self.db.add(response)
        post.processed = True
        self.db.commit()
        return response
