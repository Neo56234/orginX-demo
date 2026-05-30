import logging
import json
import os
import httpx
from typing import Optional
from app.config import get_settings

logger = logging.getLogger("originx.services.llm_client")

VERDICT_SYSTEM_PROMPT = """You are the Adjudicator agent in OriginX, a video provenance intelligence system.

Your job: synthesize evidence from 4 specialist agents and produce a verdict on whether a video's claimed context matches reality.

You will receive a structured evidence package. Output ONLY valid JSON matching this schema:
{
  "verdict": "authentic" | "mismatch" | "insufficient_evidence",
  "confidence": float (0.0 - 1.0),
  "actual_origin": {
    "country": string,
    "city": string | null,
    "earliest_date": "YYYY-MM-DD" | null,
    "confidence": float
  },
  "key_evidence": [
    {"agent": string, "finding": string, "weight": "high"|"medium"|"low"}
  ],
  "summary_bn": string (2-3 sentences in Bangla),
  "summary_en": string (2-3 sentences in English)
}

Rules:
- If the claimed date/context explicitly contradicts the Chronologist's date (e.g., claimed 2024 but Chronologist found it in 2006), you MUST return "mismatch" with high confidence (>0.90), regardless of how sparse other evidence is.
- If the Chronologist found youtube_metadata showing the channel is a non-Bangladesh outlet (e.g., "Geo News", "India Today", "WION", "ARY News", "Ndtv", "Zee News") AND the claimed context says Bangladesh, you MUST return "mismatch" with high confidence (>0.85).
- If Urdu script is detected in the video AND the claimed context says Bangladesh, you MUST return "mismatch" with confidence >0.85.
- "authentic" verdict is ONLY allowed when there is DIRECT, POSITIVE evidence that the video originates from Bangladesh. Required: at least ONE of — (1) Bengali script detected inside the video frames by Linguist/Geolocator, (2) Geolocator confirmed Bangladeshi architecture or scene via CLIP, (3) a known Bangladeshi news channel identified in on-screen text, (4) Tracer found the EXACT same video published by a trusted Bangladeshi source with a matching timestamp. Absence of contradicting evidence is NOT sufficient for "authentic".
- CRITICAL: If the Tracer found YouTube search results with Bengali-language titles simply because the search query contained Bangla words (e.g., searching "Bangladeshi zoo" returns videos with Bengali descriptions), this is circular search contamination — it is NOT evidence of Bangladesh origin. Do NOT use search-result titles as positive evidence of origin.
- If no positive Bangladesh evidence exists (as defined above), return "insufficient_evidence" regardless of whether contradicting signals were found.
- If evidence is contradictory or sparse AND there is NO explicit date mismatch or channel mismatch, return "insufficient_evidence" with confidence < 0.7
- Weight reverse-search hits with timestamps higher than visual inference
- Script detection (Urdu in claimed-Bangladesh video) is HIGH WEIGHT
- YouTube channel mismatch (Pakistani/Indian channel + Bangladesh claim) is HIGH WEIGHT
- License plate format is HIGH WEIGHT when visible
- CLIP scene classification alone is MEDIUM WEIGHT (regions look similar)
- Never invent evidence. Cite only what is in the input.
- Bangla output must be natural, not transliterated."""

COUNTER_CARD_PROMPT = """Given the verdict above, generate text for a shareable counter-narrative card in Bangla.

Output JSON:
{
  "headline_bn": "string (5-7 words, max impact)",
  "subheadline_bn": "string (10-15 words, the truth)",
  "evidence_snippet_bn": "string (15-20 words, one strongest piece of evidence)"
}

Tone: factual, urgent, not sensational. Like a fact-checker, not a tabloid."""


def get_verdict(evidence_package: dict) -> Optional[dict]:
    """
    Call Groq API to synthesize agent evidence into a verdict.
    Uses LLaMA 3.3 70B Versatile for JSON output.
    """
    settings = get_settings()
    groq_api_key = settings.groq_api_key

    if not groq_api_key:
        logger.warning("GROQ_API_KEY not set — skipping LLM verdict")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "system",
                    "content": VERDICT_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": json.dumps(evidence_package, indent=2, default=str)
                }
            ],
            "temperature": 0.1
        }
        
        resp = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
        
    except Exception as e:
        logger.error("Groq verdict call failed: %s", e)
        return None


def get_counter_card_text(verdict: dict) -> Optional[dict]:
    """
    Call Groq API to generate Bangla counter-narrative card text.
    """
    settings = get_settings()
    groq_api_key = settings.groq_api_key

    if not groq_api_key:
        logger.warning("GROQ_API_KEY not set — skipping counter card generation")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "response_format": {"type": "json_object"},
            "messages": [
                {
                    "role": "user",
                    "content": f"{COUNTER_CARD_PROMPT}\n\nVerdict:\n{json.dumps(verdict, indent=2, default=str)}"
                }
            ],
            "temperature": 0.3
        }
        
        resp = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=20)
        resp.raise_for_status()
        
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
        
    except Exception as e:
        logger.error("Counter card text generation failed: %s", e)
        return None
