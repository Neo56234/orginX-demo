import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import KnownCase, Investigation, FrameEmbedding
from app.services.phash import hamming_distance

def main():
    db = SessionLocal()
    
    # Get the KnownCase for Pakistan video
    kc = db.query(KnownCase).filter(KnownCase.debunk_url.like('%qUIej1jVrpI%')).first()
    print(f"DB pHash for '{kc.title_en}': {kc.sample_phash}")
    
    # Get the latest investigation
    inv = db.query(Investigation).order_by(Investigation.started_at.desc()).first()
    print(f"Latest Investigation URL: {inv.video_url}")
    
    # Compare
    for frame in inv.frames:
        dist = hamming_distance(frame.phash, kc.sample_phash)
        print(f"Frame {frame.frame_index} pHash: {frame.phash} | Distance: {dist}")

    db.close()

if __name__ == "__main__":
    main()
