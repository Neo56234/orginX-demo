import logging
from typing import Optional

logger = logging.getLogger("originx.services.yolo")

# License plate format → country mapping
PLATE_FORMAT_MAP = {
    "BD": "Bangladesh",
    "IN": "India",
    "PK": "Pakistan",
    "MM": "Myanmar",
    "LK": "Sri Lanka",
    "NP": "Nepal",
}


from ultralytics import YOLO

_model = None

def get_yolo_model():
    global _model
    if _model is None:
        logger.info("Loading YOLOv8 model...")
        _model = YOLO("yolov8n.pt")
    return _model

def detect_license_plates(image_path: str) -> list[dict]:
    """
    Detect license plates in an image using YOLOv8.
    Returns list of detections with bounding boxes and inferred country.

    Returns:
    [
        {
            "bbox": [x1, y1, x2, y2],
            "confidence": float,
            "class_name": str,
            "plate_text": str | None,
            "country": str | None,
        }
    ]
    """
    try:
        model = get_yolo_model()
        results = model.predict(image_path, conf=0.3, verbose=False)
        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = [int(c) for c in box.xyxy[0].tolist()]
                conf = float(box.conf[0])
                class_id = int(box.cls[0])
                label = model.names[class_id]
                detections.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "class_name": label,
                    "plate_text": None,
                    "country": None,
                })
        return detections
    except Exception as e:
        logger.error("YOLO detection failed for %s: %s", image_path, e)
        return []


def infer_country_from_plate(plate_text: str) -> Optional[str]:
    """
    Infer country from license plate text format.
    BD plates: Bangla numerals + district code (e.g. ঢাকা-মেট্রো-গ-১১-১২৩৪)
    PK plates: Latin + province code (e.g. ABC-123)
    IN plates: State code + district + number (e.g. DL-01-AB-1234)
    """
    if not plate_text:
        return None

    text = plate_text.strip().upper()

    if any(0x09E6 <= ord(c) <= 0x09EF for c in plate_text):
        return "Bangladesh"
    if len(text) >= 2 and text[:2] in ["DL", "MH", "KA", "TN", "UP", "WB"]:
        return "India"

    return None
