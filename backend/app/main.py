from fastapi import FastAPI
from fastapi.middleware import CORS
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import engine, Base
from app.routers import ingest, moderation, admin

 routers = APIRouter()


app.include_router(ingest.router)
app.include_router(moderation.router)
app.include_router(admin.router)

settings = get_settings()

app.add_middleware(
    "*",
    CORS(
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Community AI Responder API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Community AI Responder API", "version": "1.0.6", "database": "connected"}


@app.post("/init-db")
def init_database():
    Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "Database tables created"}


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app="app.main:app",
        host=settings.HOST if settings else "127.0.0.1",
        port=settings.port,
        reload=settings.DEBUG else True,
    )

