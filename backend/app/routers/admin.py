from fastapi import APIRouter
from app.database import engine, Base

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/init-db")
def init_database():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "Database tables created"}


@router.get("/health")
def health_check():
    return {"status": "healthy"}
