"""Run: python seed_viral.py from the backend/ directory."""
import json
import sys
import os
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base, ViralVideo

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(ViralVideo).count()
        if existing > 0:
            print(f"Already have {existing} viral videos. Skipping.")
            return

        data_path = os.path.join(os.path.dirname(__file__), "../data/seed/viral_videos.json")
        with open(data_path, "r", encoding="utf-8") as f:
            videos = json.load(f)

        for v in videos:
            detected_at = None
            if v.get("detected_at"):
                detected_at = datetime.fromisoformat(v["detected_at"].replace("Z", "+00:00"))

            vv = ViralVideo(
                video_url=v.get("video_url"),
                thumbnail_url=v.get("thumbnail_url"),
                claim_text=v.get("claim_text"),
                claim_text_bn=v.get("claim_text_bn"),
                share_count=v.get("share_count"),
                region=v.get("region"),
                category=v.get("category"),
                detected_at=detected_at,
                is_featured=v.get("is_featured", False),
            )
            db.add(vv)

        db.commit()
        print(f"Seeded {len(videos)} viral videos.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
