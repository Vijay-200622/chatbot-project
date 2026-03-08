"""FastAPI application — main entry point for the backend."""

import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from database.db import init_db
from database.crud import seed_topics_from_json

from backend.routers import chat, practice, concept_map, mistakes, streaks, analytics, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # ── Startup ──
    logger.info("Initializing database...")
    init_db()

    # Seed NCERT topics from JSON
    topics_path = Path(settings.project_root) / "data" / "ncert_topics.json"
    if topics_path.exists():
        with open(topics_path, encoding="utf-8") as f:
            data = json.load(f)
        seed_topics_from_json(data["topics"])
        logger.info(f"Loaded {len(data['topics'])} NCERT topics.")

    logger.info("Backend ready! 🚀")
    yield
    # ── Shutdown ──
    logger.info("Shutting down...")


app = FastAPI(
    title="NCERT AI Tutor API",
    description="Hinglish/Tanglish AI tutor for NCERT Class 9-10 students",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://localhost:{settings.frontend_port}",
        f"http://127.0.0.1:{settings.frontend_port}",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(chat.router)
app.include_router(practice.router)
app.include_router(concept_map.router)
app.include_router(mistakes.router)
app.include_router(streaks.router)
app.include_router(analytics.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {
        "message": "NCERT AI Tutor API 🎓",
        "docs": "/docs",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
