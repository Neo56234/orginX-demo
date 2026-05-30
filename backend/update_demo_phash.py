import os
import sys

# Ensure app imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import KnownCase
from app.services.video_downloader import download_video
from app.services.frame_extractor import extract_frames
from app.services.phash import compute_phash

def main():
    print("Starting pHash generator for Demo Cases...")
    db = SessionLocal()
    
    # Let's get the specific demo videos we want to calculate pHash for
    # 1. Pakistan Video
    # 2. Me at the zoo
    
    demo_urls = [
        "https://www.youtube.com/watch?v=qUIej1jVrpI",
        "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    ]
    
    cases = db.query(KnownCase).filter(KnownCase.debunk_url.in_(demo_urls)).all()
    
    if not cases:
        print("Demo cases not found in the database. Make sure you ran seed_cases.py.")
        return
        
    for case in cases:
        print(f"\nProcessing: {case.title_en} ({case.debunk_url})")
        if case.sample_phash:
            print("Already has pHash. Skipping.")
            continue
            
        print("Downloading video...")
        try:
            # We use a dummy investigation_id for downloading
            video_path = download_video(case.debunk_url, f"seed_{case.id}")
            if not video_path:
                print("Failed to download video.")
                continue
                
            print("Extracting frames...")
            frames = extract_frames(video_path, f"seed_{case.id}")
            if not frames:
                print("Failed to extract frames.")
                continue
                
            # We take the middle frame to be a representative sample
            mid_index = len(frames) // 2
            target_frame = frames[mid_index]
            
            print(f"Computing pHash for frame {mid_index}...")
            phash_val = compute_phash(target_frame)
            
            if phash_val:
                case.sample_phash = phash_val
                db.commit()
                print(f"Successfully saved pHash '{phash_val}' for case ID {case.id}")
            else:
                print("Failed to compute pHash.")
                
        except Exception as e:
            print(f"Error processing case {case.id}: {str(e)}")

    db.close()
    print("\npHash generation complete!")

if __name__ == "__main__":
    main()
