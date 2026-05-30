import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.config import get_settings
from app.database import engine, Base

settings = get_settings()
logger = logging.getLogger("originx.main")


def _wait_for_db(retries: int = 15, delay: int = 3) -> None:
    """Retry DB connection — Docker DNS for 'postgres' can take a moment."""
    for attempt in range(1, retries + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connected (attempt %d/%d)", attempt, retries)
            return
        except Exception as exc:
            logger.warning(
                "Database not ready (attempt %d/%d): %s — retrying in %ds",
                attempt, retries, exc, delay,
            )
            time.sleep(delay)
    raise RuntimeError(f"Database unreachable after {retries} attempts.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create data directories
    for d in [settings.videos_dir, settings.frames_dir, settings.cards_dir]:
        os.makedirs(d, exist_ok=True)

    # Wait for postgres to be reachable (Docker DNS timing)
    _wait_for_db()

    # Enable pgvector + pg_trgm extensions
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.commit()

    # Auto-create tables in development (production uses Alembic)
    if settings.environment == "development":
        Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="OriginX API",
    description="Video Provenance Intelligence Platform — Every video has a true origin. We find it.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated counter-card images as static files
os.makedirs(settings.cards_dir, exist_ok=True)
app.mount("/cards", StaticFiles(directory=settings.cards_dir), name="cards")

# Routers — imported here to avoid circular imports at module load time
from app.api import analyze, stream, investigation, cases, dashboard, whatsapp, chat  # noqa: E402

app.include_router(analyze.router, prefix="/api")
app.include_router(stream.router, prefix="/api")
app.include_router(investigation.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(whatsapp.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/health", tags=["meta"])
async def health():
    return {
        "status": "ok",
        "version": "0.1.0",
        "environment": settings.environment,
    }
