"""Run: python seed_trust_graph.py from the backend/ directory."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models import Base, SourceCredibility

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(SourceCredibility).count()
        if existing > 0:
            print(f"Already have {existing} sources. Skipping.")
            return

        data_path = os.path.join(os.path.dirname(__file__), "../data/seed/source_credibility.json")
        with open(data_path, "r", encoding="utf-8") as f:
            sources = json.load(f)

        for s in sources:
            src = SourceCredibility(
                platform=s["platform"],
                source_identifier=s["source_identifier"],
                display_name=s["display_name"],
                total_shared=s["total_shared"],
                flagged_count=s["flagged_count"],
                credibility_score=s["credibility_score"],
            )
            db.add(src)

        db.commit()
        print(f"Seeded {len(sources)} sources.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
