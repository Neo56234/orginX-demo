import logging
from typing import Optional

logger = logging.getLogger("originx.services.phash")

HAMMING_THRESHOLD = 10


def compute_phash(image_path: str) -> Optional[str]:
    """
    Compute perceptual hash (pHash) for an image using imagehash.
    Returns hex string of hash, or None on failure.

    Phase 1 implementation:
    - Load image with Pillow
    - Compute imagehash.phash(image)
    - Return str(hash)
    """

    # ── Phase 1: uncomment and test ────────────────────────────────────────
    from PIL import Image
    import imagehash
    try:
        img = Image.open(image_path).convert("RGB")
        return str(imagehash.phash(img))
    except Exception as e:
        logger.error("pHash failed for %s: %s", image_path, e)
        return None
    # ──────────────────────────────────────────────────────────────────────


def hamming_distance(hash1: str, hash2: str) -> int:
    """
    Compute Hamming distance between two pHash hex strings.
    Lower = more similar. 0 = identical. > 10 = different video.
    """
    # ── Phase 1: uncomment and test ────────────────────────────────────────
    import imagehash
    return imagehash.hex_to_hash(hash1) - imagehash.hex_to_hash(hash2)
    # ──────────────────────────────────────────────────────────────────────


def is_duplicate(hash1: str, hash2: str) -> bool:
    return hamming_distance(hash1, hash2) <= HAMMING_THRESHOLD
