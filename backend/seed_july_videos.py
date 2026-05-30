"""
Seed July 2024 Bangladesh movement videos into known_cases with pHash.
Run inside the worker container:
  python seed_july_videos.py
"""
import os
import sys
import subprocess
import tempfile
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("seed_july")

sys.path.insert(0, "/app")

from app.database import SessionLocal
from app.models import KnownCase
from app.services.phash import compute_phash

INCIDENTS = [
    {
        "video_path": "/tmp/seed_videos/video1.mp4",
        "title_bn": "ছাদের ওপর পুলিশ ও ছাত্রলীগের যোগসাজশে গুলি — কোটা আন্দোলন জুলাই ২০২৪",
        "title_en": "Police and Chhatra League shooting from rooftop during Bangladesh quota reform protests - July 2024",
        "false_claim_bn": "বাংলাদেশে এখনই গুলি চলছে — আজকের ঘটনা",
        "false_claim_en": "Shooting happening right now in Bangladesh - today's incident",
        "actual_origin_country": "Bangladesh",
        "actual_origin_city": "Dhaka",
        "actual_origin_date": "2024-07-19",
        "debunk_source": "july_movement_2024",
        "debunk_url": None,
        "keywords": ["quota reform", "july 2024", "chhatra league", "police", "shooting", "rooftop", "কোটা আন্দোলন", "ছাত্রলীগ", "গুলি"],
    },
    {
        "video_path": "/tmp/seed_videos/video2.mp4",
        "title_bn": "রামগঞ্জে নিরস্ত্র ছাত্রদের ওপর পুলিশের উপস্থিতিতে ছাত্রলীগের হামলা — জুলাই ২০২৪",
        "title_en": "Chhatra League attacks unarmed students in Ramganj with police present - July 2024",
        "false_claim_bn": "বাংলাদেশে ছাত্রদের ওপর হামলা হচ্ছে — আজকের ঘটনা",
        "false_claim_en": "Students being attacked in Bangladesh right now - today's incident",
        "actual_origin_country": "Bangladesh",
        "actual_origin_city": "Ramganj, Lakshmipur",
        "actual_origin_date": "2024-07-18",
        "debunk_source": "july_movement_2024",
        "debunk_url": None,
        "keywords": ["ramganj", "lakshmipur", "chhatra league", "unarmed students", "july 2024", "রামগঞ্জ", "নিরস্ত্র ছাত্র", "ছাত্রলীগ"],
    },
    {
        "video_path": "/tmp/seed_videos/video3.mp4",
        "title_bn": "৪ আগস্ট কুমিল্লায় ছাত্রলীগের তাণ্ডব — নিরস্ত্র ছাত্রছাত্রীদের ওপর হামলা",
        "title_en": "Chhatra League rampage against unarmed students in Cumilla - 4 August 2024",
        "false_claim_bn": "বাংলাদেশে আজকে ছাত্রদের ওপর হামলা হচ্ছে",
        "false_claim_en": "Students being attacked in Bangladesh today - ongoing incident",
        "actual_origin_country": "Bangladesh",
        "actual_origin_city": "Cumilla",
        "actual_origin_date": "2024-08-04",
        "debunk_source": "july_movement_2024",
        "debunk_url": None,
        "keywords": ["cumilla", "comilla", "chhatra league", "4 august", "2024", "কুমিল্লা", "৪ আগস্ট", "ছাত্রলীগ", "তাণ্ডব"],
    },
]


def extract_frames(video_path: str, out_dir: str, count: int = 6) -> list[str]:
    """Extract evenly spaced frames from video using ffmpeg."""
    os.makedirs(out_dir, exist_ok=True)
    # Get video duration
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    try:
        duration = float(probe.stdout.strip())
    except Exception:
        duration = 30.0

    interval = duration / (count + 1)
    frame_paths = []
    for i in range(count):
        ts = interval * (i + 1)
        out_path = os.path.join(out_dir, f"frame_{i:02d}.jpg")
        subprocess.run(
            ["ffmpeg", "-ss", str(ts), "-i", video_path,
             "-frames:v", "1", "-q:v", "2", out_path, "-y"],
            capture_output=True
        )
        if os.path.exists(out_path):
            frame_paths.append(out_path)

    return frame_paths


def all_phashes(frame_paths: list[str]) -> list[str]:
    """Compute pHash for all frames, return all unique non-None values."""
    hashes = []
    for fp in frame_paths:
        h = compute_phash(fp)
        if h and h not in hashes:
            hashes.append(h)
    return hashes


def main():
    db = SessionLocal()
    try:
        for idx, incident in enumerate(INCIDENTS, 1):
            video_path = incident["video_path"]
            logger.info("Processing video %d: %s", idx, video_path)

            if not os.path.exists(video_path):
                logger.error("Video not found: %s — skipping", video_path)
                continue

            # Extract frames
            with tempfile.TemporaryDirectory() as tmpdir:
                frames = extract_frames(video_path, tmpdir, count=6)
                logger.info("  Extracted %d frames", len(frames))

                if not frames:
                    logger.error("  No frames extracted — skipping")
                    continue

                phashes = all_phashes(frames)
                logger.info("  pHashes (%d): %s", len(phashes), phashes)

            # Check if this case already exists (by title_en)
            existing = db.query(KnownCase).filter(
                KnownCase.title_en == incident["title_en"]
            ).first()

            if existing:
                existing.sample_phash = phashes[0] if phashes else None
                existing.sample_phashes = phashes
                logger.info("  Updated existing known_case id=%d with %d phashes", existing.id, len(phashes))
            else:
                from datetime import date
                origin_date = None
                if incident.get("actual_origin_date"):
                    y, m, d = incident["actual_origin_date"].split("-")
                    origin_date = date(int(y), int(m), int(d))

                case = KnownCase(
                    title_bn=incident["title_bn"],
                    title_en=incident["title_en"],
                    false_claim_bn=incident["false_claim_bn"],
                    false_claim_en=incident["false_claim_en"],
                    actual_origin_country=incident["actual_origin_country"],
                    actual_origin_city=incident["actual_origin_city"],
                    actual_origin_date=origin_date,
                    debunk_source=incident["debunk_source"],
                    debunk_url=incident.get("debunk_url"),
                    sample_phash=phashes[0] if phashes else None,
                    sample_phashes=phashes,
                    keywords=incident.get("keywords", []),
                )
                db.add(case)
                logger.info("  Inserted new known_case with %d phashes", len(phashes))

        db.commit()
        logger.info("Done. All 3 incidents seeded.")

        # Verify
        cases = db.query(KnownCase).filter(
            KnownCase.debunk_source == "july_movement_2024"
        ).all()
        logger.info("Verified %d july_movement_2024 cases in DB:", len(cases))
        for c in cases:
            logger.info("  [%d] %s | phashes=%d", c.id, c.title_en[:60], len(c.sample_phashes or []))

    finally:
        db.close()


if __name__ == "__main__":
    main()
