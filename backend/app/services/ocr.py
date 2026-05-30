import logging
import threading

logger = logging.getLogger("originx.services.ocr")

import easyocr

_reader_bn = None   # Bengali + English
_reader_ur = None   # Urdu + English (loaded lazily)

_lock_bn = threading.Lock()
_lock_ur = threading.Lock()


def _get_reader_bn():
    global _reader_bn
    with _lock_bn:
        if _reader_bn is None:
            logger.info("Initializing EasyOCR Bengali reader...")
            _reader_bn = easyocr.Reader(['en', 'bn'], gpu=False)
    return _reader_bn


def _get_reader_ur():
    global _reader_ur
    with _lock_ur:
        if _reader_ur is None:
            logger.info("Initializing EasyOCR Urdu reader...")
            _reader_ur = easyocr.Reader(['en', 'ur'], gpu=False)
    return _reader_ur


def extract_text(frame_path: str) -> dict:
    """
    Run EasyOCR on a frame image using Bengali and Urdu readers.
    Merges results — catches both Bengali text and Urdu/Arabic news tickers.

    Returns:
    {
        "raw_text": str,
        "blocks": [{"text": str, "confidence": float, "bbox": [x1,y1,x2,y2]}],
        "detected_scripts": [str],
    }
    """
    blocks = []
    seen_texts: set = set()

    for reader in (_get_reader_bn(), _get_reader_ur()):
        try:
            for r in reader.readtext(frame_path, detail=1):
                text = (r[1] or "").strip()
                if not text or text.lower() in seen_texts:
                    continue
                seen_texts.add(text.lower())
                flat_bbox = [int(c) for coord in r[0] for c in coord]
                blocks.append({"text": text, "confidence": float(r[2]), "bbox": flat_bbox})
        except Exception as e:
            logger.warning("OCR reader failed on %s: %s", frame_path, e)

    raw_text = " ".join(b["text"] for b in blocks)
    from app.utils.language import detect_scripts
    detected_scripts = detect_scripts(raw_text)

    return {"raw_text": raw_text, "blocks": blocks, "detected_scripts": detected_scripts}



