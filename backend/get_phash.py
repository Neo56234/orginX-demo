import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from app.services.frame_extractor import extract_frames
from app.services.phash import compute_phash

video_path = sys.argv[1]
frames = extract_frames(video_path, "test")
mid = frames[len(frames)//2]
print("PHASH:", compute_phash(mid))
