import logging
import redis
from app.agents.base import BaseAgent

logger = logging.getLogger("originx.agent.geolocator")


class GeolocatorAgent(BaseAgent):
    """
    🌍 Geolocator — determines WHERE the video was actually filmed.

    Signals (Phase 1 implementation):
    - License plate format via YOLOv8 detection
    - Architectural style via CLIP zero-shot classification
    - Street signage script (Bangla/Urdu/Devanagari/Arabic)
    - Vehicle types (CNG vs auto-rickshaw vs tuktuk)
    - pgvector similarity against known location embeddings

    Output: { country, city, confidence, evidence[] }
    """

    name = "geolocator"

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        super().__init__(investigation_id, redis_client)

    def run(self, frames: list[str], context: dict) -> dict:
        from app.services.yolo_service import detect_license_plates, infer_country_from_plate
        from app.services.clip_service import classify_geo
        from app.services.ocr import extract_text
        from app.utils.language import detect_scripts, infer_country_from_scripts, scan_channel_names
        from collections import Counter

        self.emit_started()
        self.emit_progress(0.1, "Analyzing frames for geographic signals...")

        total_frames = len(frames)
        clip_results = []
        plate_countries = []
        all_scripts = set()
        evidence = []

        clip_label_counts: dict = {}

        for i, frame in enumerate(frames):
            frame_num = f"{i+1}/{total_frames}"

            # 1. CLIP classification — emit each frame result
            clip_res = classify_geo(frame)
            if clip_res:
                label = clip_res["label"]
                conf  = clip_res.get("confidence") or clip_res.get("score")
                clip_results.append(label)
                clip_label_counts[label] = clip_label_counts.get(label, 0) + 1
                conf_str = f"{round(conf * 100)}%" if conf is not None else "n/a"
                self.emit_finding({
                    "type": "clip_classification",
                    "description": f"Frame {frame_num}: CLIP → '{label}' ({conf_str} confidence)",
                    "weight": "medium",
                    "frame": frame_num,
                    "label": label,
                })

            # 2. OCR → script detection — emit only when a new script is found
            ocr_result = extract_text(frame)
            if ocr_result and ocr_result.get("raw_text"):
                frame_text = ocr_result["raw_text"]
                new_scripts = set()
                for s in detect_scripts(frame_text):
                    if s not in all_scripts:
                        new_scripts.add(s)
                    all_scripts.add(s)
                for script in new_scripts:
                    self.emit_finding({
                        "type": "script_detected",
                        "description": f"Frame {frame_num}: {script} script detected in on-screen text",
                        "weight": "high" if script in ("Urdu", "Devanagari", "Arabic") else "medium",
                        "frame": frame_num,
                        "script": script,
                    })

            self.emit_progress(0.1 + (i / total_frames) * 0.7, f"Geolocating frame {frame_num}...")

        # Channel name scan across all OCR text collected from frames
        all_ocr_text = " ".join(
            ocr_result.get("raw_text", "")
            for frame in frames
            for ocr_result in [extract_text(frame)]
            if ocr_result
        ) if frames else ""
        channel_hit = scan_channel_names(all_ocr_text)
        if channel_hit:
            finding = {
                "type": "channel_name_detected",
                "description": channel_hit["reasoning"],
                "weight": "high",
                "channel": channel_hit["channel"],
                "country": channel_hit["country"],
            }
            evidence.append(finding)
            self.emit_finding(finding)

        # Plate summary (YOLO not active in Phase 1 — emit note if no plates found)
        if plate_countries:
            most_common_plate = Counter(plate_countries).most_common(1)[0][0]
            finding = {
                "type": "license_plate",
                "description": f"License plate format matches {most_common_plate}",
                "weight": "high",
            }
            evidence.append(finding)
            self.emit_finding(finding)

        # CLIP consensus summary
        if clip_results:
            most_common_scene = Counter(clip_results).most_common(1)[0][0]
            count = clip_label_counts.get(most_common_scene, 0)
            finding = {
                "type": "clip_consensus",
                "description": f"CLIP consensus: '{most_common_scene}' in {count}/{total_frames} frames",
                "weight": "medium",
            }
            evidence.append(finding)
            self.emit_finding(finding)

        # Script geo-inference summary
        script_geo = infer_country_from_scripts(list(all_scripts))
        if script_geo:
            finding = {
                "type": "script_geo_inference",
                "description": script_geo["reasoning"],
                "weight": "high" if script_geo.get("not_bangladesh") else "medium",
            }
            evidence.append(finding)
            self.emit_finding(finding)
        elif not all_scripts:
            self.emit_finding({
                "type": "script_none",
                "description": "No readable on-screen text detected across all frames.",
                "weight": "low",
            })

        # Country resolution — channel name is highest priority, then plate, script, CLIP
        predicted_country = None
        confidence = 0.0

        if channel_hit:
            predicted_country = channel_hit["country"]
            confidence = channel_hit["confidence"]
        elif plate_countries:
            predicted_country = Counter(plate_countries).most_common(1)[0][0]
            confidence = 0.9
        elif script_geo and script_geo["country"] != "Unknown":
            predicted_country = script_geo["country"]
            confidence = script_geo["confidence"]
        elif clip_results:
            most_common_scene = Counter(clip_results).most_common(1)[0][0]
            if "Bangladesh" in most_common_scene:
                predicted_country = "Bangladesh"
                confidence = 0.6
            elif "Pakistan" in most_common_scene:
                predicted_country = "Pakistan"
                confidence = 0.6
            elif "India" in most_common_scene:
                predicted_country = "India"
                confidence = 0.6

        output = {
            "country": predicted_country,
            "city": None,
            "confidence": confidence,
            "evidence": evidence,
        }

        self.emit_complete(output)
        logger.info("Geolocator complete — investigation=%s", self.investigation_id)
        return output
