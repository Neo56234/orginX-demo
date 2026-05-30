"""
Seed script — loads known_cases.json and viral_videos.json into PostgreSQL.

Usage:
    docker compose exec api python seed_cases.py

Run once after `docker compose up` to populate the database.
Safe to run multiple times — skips existing records.
"""

import json
import os
import sys
from datetime import datetime

from sqlalchemy import text
from app.database import SessionLocal, engine, Base
from app.models import KnownCase, ViralVideo

SEED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "seed")
KNOWN_CASES_FILE = os.path.join(SEED_DIR, "known_cases.json")
VIRAL_VIDEOS_FILE = os.path.join(SEED_DIR, "viral_videos.json")


def ensure_extensions():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        conn.commit()
    print("✓ PostgreSQL extensions ready (vector, pg_trgm)")


def ensure_tables():
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created (if not exist)")


def seed_known_cases(db):
    if not os.path.exists(KNOWN_CASES_FILE):
        print(f"✗ File not found: {KNOWN_CASES_FILE}")
        return 0

    with open(KNOWN_CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    inserted = 0
    skipped = 0

    for case in cases:
        # Skip if already exists (match by title_en)
        exists = db.query(KnownCase).filter(
            KnownCase.title_en == case.get("title_en")
        ).first()

        if exists:
            skipped += 1
            continue

        date_str = case.get("actual_origin_date")
        origin_date = None
        if date_str:
            try:
                origin_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                pass

        record = KnownCase(
            title_en=case.get("title_en"),
            title_bn=case.get("title_bn"),
            false_claim_en=case.get("false_claim_en"),
            false_claim_bn=case.get("false_claim_bn"),
            actual_origin_country=case.get("actual_origin_country"),
            actual_origin_city=case.get("actual_origin_city"),
            actual_origin_date=origin_date,
            debunk_url=case.get("debunk_url"),
            debunk_source=case.get("debunk_source"),
            keywords=case.get("keywords", []),
        )
        db.add(record)
        inserted += 1

    db.commit()
    return inserted, skipped


def seed_viral_videos(db):
    if not os.path.exists(VIRAL_VIDEOS_FILE):
        print(f"✗ File not found: {VIRAL_VIDEOS_FILE}")
        return 0, 0

    with open(VIRAL_VIDEOS_FILE, "r", encoding="utf-8") as f:
        videos = json.load(f)

    inserted = 0
    skipped = 0

    for video in videos:
        exists = db.query(ViralVideo).filter(
            ViralVideo.video_url == video.get("video_url")
        ).first()

        if exists:
            skipped += 1
            continue

        detected_str = video.get("detected_at")
        detected_at = None
        if detected_str:
            try:
                detected_at = datetime.fromisoformat(detected_str.replace("Z", "+00:00"))
            except ValueError:
                pass

        record = ViralVideo(
            video_url=video.get("video_url"),
            thumbnail_url=video.get("thumbnail_url"),
            claim_text=video.get("claim_text"),
            claim_text_bn=video.get("claim_text_bn"),
            share_count=video.get("share_count"),
            detected_at=detected_at,
            region=video.get("region"),
            category=video.get("category"),
            is_featured=video.get("is_featured", False),
        )
        db.add(record)
        inserted += 1

    db.commit()
    return inserted, skipped


def main():
    print("\n━━━ OriginX Database Seeder ━━━\n")

    ensure_extensions()
    ensure_tables()

    db = SessionLocal()
    try:
        print("\n→ Seeding known_cases...")
        inserted, skipped = seed_known_cases(db)
        print(f"  ✓ Inserted: {inserted}  |  Skipped (already exist): {skipped}")

        print("\n→ Seeding viral_videos...")
        inserted, skipped = seed_viral_videos(db)
        print(f"  ✓ Inserted: {inserted}  |  Skipped (already exist): {skipped}")

    except Exception as e:
        print(f"\n✗ Seeding failed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

    print("\n━━━ Seeding complete! ━━━\n")


if __name__ == "__main__":
    main()
