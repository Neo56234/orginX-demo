import logging
import os
import ffmpeg
from app.config import get_settings

logger = logging.getLogger("originx.services.frame_extractor")

FRAME_COUNT = 6


def extract_frames(video_path: str, job_id: str) -> list[str]:
    """
    Extract FRAME_COUNT evenly-spaced keyframes from a video using ffmpeg.
    Returns list of absolute frame file paths.

    Phase 1 implementation:
    - Probe video duration
    - Calculate interval = duration / FRAME_COUNT
    - Extract frames at each interval as JPEG
    - Save to {DATA_DIR}/frames/{job_id}/frame_00.jpg ... frame_11.jpg
    - Return sorted list of paths
    """
    settings = get_settings()
    frames_dir = os.path.join(settings.frames_dir, job_id)
    os.makedirs(frames_dir, exist_ok=True)

    # ── Phase 1: uncomment and test ────────────────────────────────────────
    probe = ffmpeg.probe(video_path)
    duration = float(probe["format"]["duration"])
    interval = duration / FRAME_COUNT

    frame_paths = []
    for i in range(FRAME_COUNT):
        timestamp = interval * i
        out_path = os.path.join(frames_dir, f"frame_{i:02d}.jpg")
        (
            ffmpeg
            .input(video_path, ss=timestamp)
            .output(out_path, vframes=1, format="image2", vcodec="mjpeg")
            .overwrite_output()
            .run(quiet=True)
        )
        frame_paths.append(out_path)
        logger.debug("Extracted frame %d → %s", i, out_path)

    return sorted(frame_paths)
    # ──────────────────────────────────────────────────────────────────────
