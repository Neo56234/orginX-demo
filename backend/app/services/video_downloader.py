import logging
import os
import yt_dlp
from app.config import get_settings

logger = logging.getLogger("originx.services.video_downloader")


def download_video(url: str, job_id: str) -> str:
    """
    Download video from URL using yt-dlp.
    Returns local file path on success.
    Raises RuntimeError on failure.

    Supports: YouTube, Facebook, TikTok, Twitter/X, Telegram public links.

    Phase 1 implementation:
    - Configure yt-dlp with retry + format preference (mp4 max 200MB)
    - Save to {DATA_DIR}/videos/{job_id}.mp4
    - Return absolute path
    """
    settings = get_settings()
    os.makedirs(settings.videos_dir, exist_ok=True)
    if url.startswith("local://"):
        return os.path.join(settings.videos_dir, f"{job_id}.mp4")
        
    output_path = os.path.join(settings.videos_dir, f"{job_id}.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        # Prefer 720p or lower mp4 to stay under 200MB; fall back to any best format
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "retries": 3,
        "socket_timeout": 30,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".mp4")
        logger.info("Downloaded video: %s → %s", url, filename)
        return filename
