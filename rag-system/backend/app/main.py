from fastapi import FastAPI
from app.api.health import router as health_router

app = FastAPI(title="RAG System",
    description="Real-time RAG system with Private + Web-Assisted modes",
    version="1.0.0"
)

app.include_router(health_router, prefix="/api")
