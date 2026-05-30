"""
/api/chat — RAG chatbot endpoint for querying Bangladesh misinformation knowledge base.
Uses BM25 + Vector + RRF search to find relevant incidents, then Groq LLM for answer.
"""
import logging
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_db
from app.services.rag_search import search_incidents, format_context
from app.config import get_settings
import httpx

logger = logging.getLogger("originx.api.chat")
router = APIRouter(tags=["chat"])

CHAT_SYSTEM_PROMPT = """You are OriginX Assistant, an expert on video misinformation and fake news incidents in Bangladesh.

You have access to a database of verified misinformation cases — videos that were falsely shared with wrong context, wrong dates, or wrong locations.

Your job: answer the user's question using ONLY the provided incident context. Be factual, specific, and cite incident details (title, date, actual origin, false claim).

Rules:
- Answer in the same language the user asks (Bangla or English)
- If the context has relevant incidents, cite them clearly with titles and dates
- If no relevant incidents are found, say so honestly — do not invent cases
- Keep answers concise: 2-4 sentences per incident cited
- Always mention: what was falsely claimed, what the truth is, and when it actually happened
- Do not speculate beyond the provided context"""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


async def stream_chat_response(message: str, context: str, history: list[ChatMessage]):
    settings = get_settings()
    groq_api_key = settings.groq_api_key

    if not groq_api_key:
        yield "data: " + json.dumps({"content": "GROQ_API_KEY not configured."}) + "\n\n"
        return

    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]

    # Add conversation history (last 6 turns)
    for msg in history[-6:]:
        messages.append({"role": msg.role, "content": msg.content})

    # Add current user message with context injected
    user_content = f"""Relevant incidents from OriginX database:
---
{context}
---

User question: {message}"""
    messages.append({"role": "user", "content": user_content})

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST",
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "stream": True,
                    "temperature": 0.3,
                    "max_tokens": 800,
                },
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data = line[6:]
                    if data == "[DONE]":
                        yield "data: [DONE]\n\n"
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield "data: " + json.dumps({"content": delta}) + "\n\n"
                    except Exception:
                        continue
    except Exception as e:
        logger.error("Chat stream error: %s", e)
        yield "data: " + json.dumps({"content": f"\n\n[Error: {e}]"}) + "\n\n"


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Stream a RAG-powered chat response about Bangladesh misinformation incidents.
    """
    # Search for relevant incidents
    results = search_incidents(db, req.message, top_k=5)
    context = format_context(results)
    logger.info("Chat query='%s' → %d incidents found", req.message[:60], len(results))

    return StreamingResponse(
        stream_chat_response(req.message, context, req.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Non-streaming chat endpoint — returns full response at once.
    """
    settings = get_settings()
    groq_api_key = settings.groq_api_key

    results = search_incidents(db, req.message, top_k=5)
    context = format_context(results)

    if not groq_api_key:
        return {"answer": "GROQ_API_KEY not configured.", "incidents_found": len(results)}

    messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
    for msg in req.history[-6:]:
        messages.append({"role": msg.role, "content": msg.content})

    user_content = f"""Relevant incidents from OriginX database:
---
{context}
---

User question: {req.message}"""
    messages.append({"role": "user", "content": user_content})

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 800,
                },
            )
            resp.raise_for_status()
            answer = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error("Chat error: %s", e)
        answer = f"Error generating response: {e}"

    return {
        "answer": answer,
        "incidents_found": len(results),
        "sources": [
            {
                "title": r.get("title_en"),
                "date": str(r.get("actual_origin_date") or ""),
                "origin": r.get("actual_origin_country"),
                "url": r.get("debunk_url"),
            }
            for r in results
        ],
    }
