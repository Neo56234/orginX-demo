from abc import ABC, abstractmethod
from typing import Any
import json
import redis


class BaseAgent(ABC):
    name: str  # set by subclass

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        self.investigation_id = investigation_id
        self.redis = redis_client
        self.channel = f"investigation:{investigation_id}"

    def _publish(self, event_type: str, payload: dict):
        msg = json.dumps({
            "agent": self.name,
            "event": event_type,
            "data": payload,
        })
        self.redis.publish(self.channel, msg)

    def emit_started(self):
        self._publish("agent_started", {})

    def emit_progress(self, progress: float, status_text: str = ""):
        self._publish("agent_progress", {"progress": progress, "text": status_text})

    def emit_finding(self, finding: dict):
        self._publish("agent_finding", finding)

    def emit_complete(self, output: dict):
        self._publish("agent_complete", {"output": output})

    def emit_failed(self, error: str):
        self._publish("agent_failed", {"error": error})

    @abstractmethod
    def run(self, frames: list[str], context: dict) -> dict:
        """Execute the agent. Must return structured output."""
        ...
