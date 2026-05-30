import subprocess
import json
import os
import logging

logger = logging.getLogger(__name__)

FPCALC_PATH = os.getenv("FPCALC_PATH", "fpcalc")


def extract_fingerprint(video_path: str) -> dict | None:
    """
    Extract audio fingerprint from a video file using fpcalc (Chromaprint).
    Returns {"duration": float, "fingerprint": str} or None on failure.
    """
    if not os.path.exists(video_path):
        return None

    try:
        result = subprocess.run(
            [FPCALC_PATH, "-json", "-length", "120", video_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return {
                "duration": data.get("duration"),
                "fingerprint": data.get("fingerprint"),
            }
        else:
            logger.warning(f"fpcalc failed for {video_path}: {result.stderr}")
    except FileNotFoundError:
        logger.warning("fpcalc not found — audio fingerprinting disabled. Install Chromaprint.")
    except subprocess.TimeoutExpired:
        logger.warning(f"fpcalc timed out for {video_path}")
    except Exception as e:
        logger.warning(f"Audio fingerprint extraction failed: {e}")

    return None


def fingerprints_match(fp1: str, fp2: str, threshold: float = 0.85) -> bool:
    """
    Simple fingerprint comparison using Hamming distance on compressed strings.
    Returns True if they appear to be the same audio.
    """
    if not fp1 or not fp2:
        return False
    try:
        import acoustid
        score = acoustid.compare_fingerprints(fp1, fp2)
        return score >= threshold
    except Exception:
        # Fallback: exact string match
        return fp1 == fp2
