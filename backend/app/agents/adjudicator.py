import logging
import json
import redis
from app.agents.base import BaseAgent
from app.services.llm_client import get_verdict, get_counter_card_text

logger = logging.getLogger("originx.agent.adjudicator")


class AdjudicatorAgent(BaseAgent):
    """
    ⚖️ Adjudicator — synthesizes all agent evidence into a final verdict.

    Receives structured output from Geolocator, Chronologist, Tracer, Linguist.
    Calls Groq API (LLaMA 3.3 70B) via llm_client.

    Output: { verdict, confidence, actual_origin, key_evidence, summary_bn, summary_en, card_text }
    """

    name = "adjudicator"

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        super().__init__(investigation_id, redis_client)

    def run(self, frames: list[str], context: dict) -> dict:
        import time

        self.emit_started()
        self.emit_progress(0.2, "Synthesizing evidence from all agents...")

        agent_outputs = context.get("agent_outputs", {})
        video_url = context.get("video_url", "")
        claimed_context = context.get("claimed_context", "")

        evidence_dict = {
            "investigation_id": self.investigation_id,
            "video_url": video_url,
            "claimed_context": claimed_context,
            "geolocator": agent_outputs.get("geolocator"),
            "chronologist": agent_outputs.get("chronologist"),
            "tracer": agent_outputs.get("tracer"),
            "linguist": agent_outputs.get("linguist"),
        }

        self.emit_progress(0.4, "Calling LLM for verdict synthesis...")
        verdict_json = get_verdict(evidence_dict)

        if not verdict_json:
            verdict_json = {
                "verdict": "insufficient_evidence",
                "confidence": 0.0,
                "actual_origin": {
                    "country": None,
                    "city": None,
                    "earliest_date": None,
                    "confidence": 0.0,
                },
                "key_evidence": [],
                "summary_bn": "সিস্টেম এরর: LLM API কাজ করছে না।",
                "summary_en": "System Error: LLM API failed.",
            }

        self.emit_progress(0.6, "Weighing evidence — streaming reasoning chain...")

        # Stream each key evidence item one by one for live reasoning effect
        key_evidence = verdict_json.get("key_evidence", [])
        for item in key_evidence:
            agent_label = item.get("agent", "unknown").upper()
            finding_text = item.get("finding", "")
            weight = item.get("weight", "low")
            self.emit_finding({
                "type": "verdict_evidence",
                "source_agent": item.get("agent", "unknown"),
                "description": f"[{agent_label}] {finding_text}",
                "weight": weight,
            })
            time.sleep(0.3)

        # Emit the final decision logic summary
        high_items = [e for e in key_evidence if e.get("weight") == "high"]
        med_items  = [e for e in key_evidence if e.get("weight") == "medium"]
        verdict_label = {
            "mismatch":             "MISMATCH CONFIRMED",
            "authentic":            "AUTHENTIC CONFIRMED",
            "insufficient_evidence": "INSUFFICIENT EVIDENCE",
        }.get(verdict_json["verdict"], "UNKNOWN")
        conf_pct = round(verdict_json.get("confidence", 0.0) * 100)
        parts = []
        if high_items:
            parts.append(f"{len(high_items)}× HIGH")
        if med_items:
            parts.append(f"{len(med_items)}× MED")
        weight_summary = " + ".join(parts) if parts else "no strong evidence"
        reasoning_line = f"{weight_summary} → {conf_pct}% confidence → {verdict_label}"

        self.emit_finding({
            "type": "decision_logic",
            "description": reasoning_line,
            "verdict": verdict_json["verdict"],
            "confidence": verdict_json.get("confidence", 0.0),
            "weight": "high",
            "high_count": len(high_items),
            "med_count": len(med_items),
        })

        self.emit_progress(0.9, "Generating shareable counter-narrative card...")
        card_text = get_counter_card_text(verdict_json)
        if card_text:
            verdict_json["card_text"] = card_text

        self.emit_progress(1.0, "Verdict ready.")
        self.emit_complete(verdict_json)
        logger.info("Adjudicator complete — investigation=%s", self.investigation_id)
        return verdict_json
