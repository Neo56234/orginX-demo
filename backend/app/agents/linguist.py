import logging
import redis
from app.agents.base import BaseAgent

logger = logging.getLogger("originx.agent.linguist")


class LinguistAgent(BaseAgent):
    """
    🗣️ Linguist — reads all text in the video and infers origin from language.

    Signals (Phase 1 implementation):
    - EasyOCR multi-script extraction (Bangla, Hindi, Urdu, Arabic, English)
    - Script → country inference (Urdu → not BD; Devanagari → likely India)
    - langdetect for language detection
    - Named entity extraction (place names, people, events)

    Output: { detected_scripts: [], ocr_texts: [], geo_inference, entities[], evidence[] }
    """

    name = "linguist"

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        super().__init__(investigation_id, redis_client)

    def run(self, frames: list[str], context: dict) -> dict:
        from app.services.ocr import extract_text
        from app.utils.language import detect_scripts, infer_country_from_scripts, extract_date_patterns, scan_channel_names

        self.emit_started()
        self.emit_progress(0.1, "Extracting text from frames...")

        all_text = []
        all_scripts: set = set()
        dates_found: set = set()
        evidence = []

        total = len(frames)
        for i, frame in enumerate(frames):
            frame_num = f"{i+1}/{total}"
            ocr_result = extract_text(frame)
            if ocr_result and ocr_result.get("raw_text"):
                frame_text = ocr_result["raw_text"]
                all_text.append(frame_text)

                # Emit each newly discovered script immediately
                for s in detect_scripts(frame_text):
                    if s not in all_scripts:
                        all_scripts.add(s)
                        self.emit_finding({
                            "type": "script_detected",
                            "description": f"Frame {frame_num}: {s} script found in on-screen text",
                            "weight": "high" if s in ("Urdu", "Devanagari", "Arabic") else "medium",
                            "script": s,
                            "frame": frame_num,
                        })

                # Emit each newly discovered date pattern immediately
                for d in extract_date_patterns(frame_text):
                    if d not in dates_found:
                        dates_found.add(d)
                        self.emit_finding({
                            "type": "date_in_text",
                            "description": f"Frame {frame_num}: date pattern found in text — \"{d}\"",
                            "weight": "medium",
                            "date": d,
                            "frame": frame_num,
                        })

                # Emit a snippet of meaningful OCR text (first non-trivial line)
                snippet = frame_text.strip()[:80]
                if len(snippet) > 10:
                    self.emit_finding({
                        "type": "ocr_text",
                        "description": f"Frame {frame_num}: OCR text — \"{snippet}\"",
                        "weight": "low",
                        "frame": frame_num,
                    })

            self.emit_progress(0.1 + (i / total) * 0.75, f"OCR on frame {frame_num}...")

        # Channel name scan — strongest raw-video signal
        combined_text = " ".join(all_text)
        channel_hit = scan_channel_names(combined_text)
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

        script_list = list(all_scripts)
        geo_inf = infer_country_from_scripts(script_list)

        if geo_inf:
            finding = {
                "type": "script_geo_inference",
                "description": geo_inf["reasoning"],
                "weight": "high" if geo_inf.get("not_bangladesh") else "medium",
            }
            evidence.append(finding)
            self.emit_finding(finding)
        elif not all_scripts:
            self.emit_finding({
                "type": "script_none",
                "description": "No readable text or scripts detected across all frames.",
                "weight": "low",
            })

        if dates_found:
            date_list = ", ".join(sorted(dates_found))
            finding = {
                "type": "dates_summary",
                "description": f"All dates found in video text: {date_list}",
                "weight": "medium",
            }
            evidence.append(finding)
            self.emit_finding(finding)

        output = {
            "detected_scripts": script_list,
            "ocr_texts": list(set(all_text)),
            "geo_inference": geo_inf["country"] if geo_inf else None,
            "geo_confidence": geo_inf["confidence"] if geo_inf else 0.0,
            "entities": list(dates_found),
            "evidence": evidence,
        }

        self.emit_complete(output)
        logger.info("Linguist complete — investigation=%s", self.investigation_id)
        return output
