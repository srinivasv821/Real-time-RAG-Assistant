from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.db.session import engine, Base

app = FastAPI(title="RAG System",
    description="Real-time RAG system with Private + Web-Assisted modes",
    version="1.0.0"
)

# Create DB tables at start up
Base.metadata.create_all(bind=engine)

app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
