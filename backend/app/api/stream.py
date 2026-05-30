import json
import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import redis.asyncio as aioredis

from app.config import get_settings

router = APIRouter()


@router.get("/stream/{investigation_id}")
async def stream(investigation_id: str, request: Request):
    """
    SSE endpoint — relays Redis pub/sub messages to the browser in real time.
    Each agent publishes to channel `investigation:{id}` as it runs.
    """
    settings = get_settings()
    channel = f"investigation:{investigation_id}"

    async def event_generator():
        # Send an initial keep-alive so the browser knows the connection opened
        yield ": keep-alive\n\n"

        client = None
        pubsub = None
        try:
            client = aioredis.from_url(settings.redis_url, socket_connect_timeout=5)
            pubsub = client.pubsub()
            await pubsub.subscribe(channel)
        except Exception as exc:
            error_payload = json.dumps({"error": f"Stream unavailable: {exc}"})
            yield f"event: stream_error\ndata: {error_payload}\n\n"
            return

        try:
            while True:
                if await request.is_disconnected():
                    break

                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=1.0
                )
                if message and message.get("data"):
                    raw = message["data"]
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8")
                    try:
                        parsed = json.loads(raw)
                        event_type = parsed.get("event", "message")
                        yield f"event: {event_type}\ndata: {raw}\n\n"
                        if event_type == "investigation_complete":
                            break
                    except json.JSONDecodeError:
                        continue

                await asyncio.sleep(0.05)
        except Exception as exc:
            error_payload = json.dumps({"error": str(exc)})
            yield f"event: stream_error\ndata: {error_payload}\n\n"
        finally:
            if pubsub:
                await pubsub.unsubscribe(channel)
                await pubsub.aclose()
            if client:
                await client.aclose()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
