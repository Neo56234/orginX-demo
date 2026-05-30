from __future__ import annotations
from datetime import datetime, date
from typing import Optional, Any
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    video_url: Optional[str] = None
    claimed_context: Optional[str] = None


class AnalyzeResponse(BaseModel):
    investigation_id: str
    stream_url: str
    share_url: str


class AgentFinding(BaseModel):
    type: str
    value: Any
    confidence: Optional[float] = None
    frame_ref: Optional[str] = None
    bbox: Optional[list[int]] = None


class InvestigationOut(BaseModel):
    id: str
    status: str
    video_url: Optional[str] = None
    share_slug: Optional[str] = None
    verdict: Optional[str] = None
    confidence: Optional[float] = None
    summary_bn: Optional[str] = None
    summary_en: Optional[str] = None
    actual_origin_country: Optional[str] = None
    actual_origin_city: Optional[str] = None
    actual_origin_date: Optional[date] = None
    claimed_location: Optional[str] = None
    claimed_date: Optional[date] = None
    agent_outputs: Optional[dict] = None
    evidence: Optional[list] = None
    counter_card_path: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None

    model_config = {"from_attributes": True}


class KnownCaseOut(BaseModel):
    id: int
    title_bn: Optional[str] = None
    title_en: Optional[str] = None
    false_claim_bn: Optional[str] = None
    false_claim_en: Optional[str] = None
    actual_origin_country: Optional[str] = None
    actual_origin_city: Optional[str] = None
    actual_origin_date: Optional[date] = None
    debunk_url: Optional[str] = None
    debunk_source: Optional[str] = None

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
