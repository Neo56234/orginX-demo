from typing import Generator
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import get_settings, Settings
import redis as redis_lib


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis() -> redis_lib.Redis:
    settings = get_settings()
    return redis_lib.from_url(settings.redis_url, decode_responses=False)


def get_settings_dep() -> Settings:
    return get_settings()
