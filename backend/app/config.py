from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/community_ai"
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/community_ai"
    
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    WEBHOOK_SECRET: str = ""
    
    JOB_QUEUE_POLL_INTERVAL: int = 5
    JOB_MAX_ATTEMPTS: int = 3
    
    QUALITY_SCORE_THRESHOLD: float = 3.0
    
    REPLY_POSTING_ENABLED: bool = False
    SKOOL_EMAIL: str = ""
    SKOOL_PASSWORD: str = ""
    
    POST_MAX_AGE_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
