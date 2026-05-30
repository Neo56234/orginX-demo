import logging
import time
import redis
from rq import Worker, Queue

from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("originx.worker")

QUEUE_NAME = "investigation_queue"

MAX_RETRIES = 15
RETRY_DELAY = 3  # seconds


def _connect_redis(redis_url: str) -> redis.Redis:
    """Connect to Redis with retry loop — Docker DNS can take a moment to resolve."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            conn = redis.from_url(redis_url, socket_connect_timeout=5)
            conn.ping()
            logger.info("Redis connected (attempt %d/%d)", attempt, MAX_RETRIES)
            return conn
        except Exception as exc:
            logger.warning(
                "Redis not ready (attempt %d/%d): %s — retrying in %ds",
                attempt, MAX_RETRIES, exc, RETRY_DELAY,
            )
            time.sleep(RETRY_DELAY)
    raise SystemExit(f"Redis unreachable at {redis_url} after {MAX_RETRIES} attempts.")


def main():
    settings = get_settings()
    conn = _connect_redis(settings.redis_url)

    queue = Queue(QUEUE_NAME, connection=conn)
    worker = Worker([queue], connection=conn)
    logger.info("OriginX RQ Worker ready — listening on queue: %s", QUEUE_NAME)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
