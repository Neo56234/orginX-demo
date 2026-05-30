import uuid
from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    String, Text, Float, Integer, Boolean,
    DateTime, Date, ARRAY, ForeignKey, UniqueConstraint, func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.database import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    video_url: Mapped[Optional[str]] = mapped_column(Text)
    video_file_path: Mapped[Optional[str]] = mapped_column(Text)
    video_phash: Mapped[Optional[str]] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)

    # Verdict (populated by Adjudicator)
    verdict: Mapped[Optional[str]] = mapped_column(String(32))
    confidence: Mapped[Optional[float]] = mapped_column(Float)
    summary_bn: Mapped[Optional[str]] = mapped_column(Text)
    summary_en: Mapped[Optional[str]] = mapped_column(Text)

    # Origin findings
    actual_origin_country: Mapped[Optional[str]] = mapped_column(String(64))
    actual_origin_city: Mapped[Optional[str]] = mapped_column(String(128))
    actual_origin_date: Mapped[Optional[date]] = mapped_column(Date)
    actual_origin_confidence: Mapped[Optional[float]] = mapped_column(Float)

    # Claimed context (from user-supplied caption)
    claimed_location: Mapped[Optional[str]] = mapped_column(Text)
    claimed_date: Mapped[Optional[date]] = mapped_column(Date)

    # Raw agent outputs
    agent_outputs: Mapped[Optional[dict]] = mapped_column(JSONB)
    evidence: Mapped[Optional[dict]] = mapped_column(JSONB)

    # Generated assets
    counter_card_path: Mapped[Optional[str]] = mapped_column(Text)
    forensic_replay_path: Mapped[Optional[str]] = mapped_column(Text)

    # Public sharing / Trust Memory
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    share_slug: Mapped[Optional[str]] = mapped_column(String(64), unique=True)

    frames: Mapped[list["FrameEmbedding"]] = relationship(back_populates="investigation", cascade="all, delete-orphan")
    agent_runs: Mapped[list["AgentRun"]] = relationship(back_populates="investigation", cascade="all, delete-orphan")


class FrameEmbedding(Base):
    __tablename__ = "frame_embeddings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE")
    )
    frame_index: Mapped[int] = mapped_column(Integer, nullable=False)
    frame_path: Mapped[str] = mapped_column(Text, nullable=False)
    phash: Mapped[str] = mapped_column(String(64), nullable=False)
    clip_embedding: Mapped[Optional[list]] = mapped_column(Vector(512))
    ocr_text: Mapped[Optional[str]] = mapped_column(Text)
    detected_scripts: Mapped[Optional[list]] = mapped_column(ARRAY(Text))
    plate_country: Mapped[Optional[str]] = mapped_column(String(8))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    investigation: Mapped["Investigation"] = relationship(back_populates="frames")


class KnownCase(Base):
    __tablename__ = "known_cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_bn: Mapped[Optional[str]] = mapped_column(Text)
    title_en: Mapped[Optional[str]] = mapped_column(Text)
    false_claim_bn: Mapped[Optional[str]] = mapped_column(Text)
    false_claim_en: Mapped[Optional[str]] = mapped_column(Text)
    actual_origin_country: Mapped[Optional[str]] = mapped_column(String(64))
    actual_origin_city: Mapped[Optional[str]] = mapped_column(String(128))
    actual_origin_date: Mapped[Optional[date]] = mapped_column(Date)
    debunk_url: Mapped[Optional[str]] = mapped_column(Text)
    debunk_source: Mapped[Optional[str]] = mapped_column(String(64))
    sample_phash: Mapped[Optional[str]] = mapped_column(String(64))
    sample_phashes: Mapped[Optional[list]] = mapped_column(ARRAY(Text))
    sample_clip_embedding: Mapped[Optional[list]] = mapped_column(Vector(512))
    text_embedding: Mapped[Optional[list]] = mapped_column(Vector(384))
    keywords: Mapped[Optional[list]] = mapped_column(ARRAY(Text))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SourceCredibility(Base):
    __tablename__ = "source_credibility"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    platform: Mapped[Optional[str]] = mapped_column(String(32))
    source_identifier: Mapped[Optional[str]] = mapped_column(Text)
    display_name: Mapped[Optional[str]] = mapped_column(Text)
    total_shared: Mapped[int] = mapped_column(Integer, default=0)
    flagged_count: Mapped[int] = mapped_column(Integer, default=0)
    credibility_score: Mapped[Optional[float]] = mapped_column(Float)
    last_flagged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    __table_args__ = (UniqueConstraint("platform", "source_identifier"),)


class ViralVideo(Base):
    __tablename__ = "viral_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    video_url: Mapped[Optional[str]] = mapped_column(Text)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(Text)
    claim_text: Mapped[Optional[str]] = mapped_column(Text)
    claim_text_bn: Mapped[Optional[str]] = mapped_column(Text)
    share_count: Mapped[Optional[int]] = mapped_column(Integer)
    detected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    region: Mapped[Optional[str]] = mapped_column(String(64))
    category: Mapped[Optional[str]] = mapped_column(String(64))
    investigation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigations.id")
    )
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    investigation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="CASCADE")
    )
    agent_name: Mapped[Optional[str]] = mapped_column(String(32))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[Optional[str]] = mapped_column(String(32))
    findings: Mapped[Optional[dict]] = mapped_column(JSONB)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    investigation: Mapped["Investigation"] = relationship(back_populates="agent_runs")

class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phash: Mapped[str] = mapped_column(String(64), nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    investigation_count: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    investigation_ids: Mapped[Optional[dict]] = mapped_column(JSONB)
    sample_claim_bn: Mapped[Optional[str]] = mapped_column(Text)
