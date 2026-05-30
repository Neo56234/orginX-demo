import json
import redis
from app.config import get_settings


def get_redis_client() -> redis.Redis:
    settings = get_settings()
    return redis.from_url(settings.redis_url, decode_responses=False)


def publish_event(
    redis_client: redis.Redis,
    investigation_id: str,
    agent: str,
    event_type: str,
    data: dict,
) -> None:
    """
    Publish a structured SSE event to the investigation's Redis channel.
    The stream.py SSE endpoint subscribes to this channel and relays to browser.
    """
    channel = f"investigation:{investigation_id}"
    msg = json.dumps({
        "agent": agent,
        "event": event_type,
        "data": data,
    })
    redis_client.publish(channel, msg)


def publish_investigation_complete(
    redis_client: redis.Redis,
    investigation_id: str,
    verdict: dict,
) -> None:
    """
    Publish the final investigation_complete event.
    This causes the SSE stream to close on the frontend.
    """
    publish_event(
        redis_client,
        investigation_id,
        agent="adjudicator",
        event_type="investigation_complete",
        data={"verdict": verdict},
    )
