import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.deps import get_db
from app.models import Investigation, ViralVideo
from app.schemas import InvestigationOut

router = APIRouter()


@router.get("/investigation/{investigation_id}", response_model=InvestigationOut)
def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    try:
        inv_uuid = uuid.UUID(investigation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investigation ID")

    inv = db.query(Investigation).filter(Investigation.id == inv_uuid).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    return InvestigationOut(
        id=str(inv.id),
        status=inv.status,
        video_url=inv.video_url,
        share_slug=inv.share_slug,
        verdict=inv.verdict,
        confidence=inv.confidence,
        summary_bn=inv.summary_bn,
        summary_en=inv.summary_en,
        actual_origin_country=inv.actual_origin_country,
        actual_origin_city=inv.actual_origin_city,
        actual_origin_date=inv.actual_origin_date,
        claimed_location=inv.claimed_location,
        claimed_date=inv.claimed_date,
        agent_outputs=inv.agent_outputs,
        evidence=inv.evidence,
        counter_card_path=inv.counter_card_path,
        started_at=inv.started_at,
        completed_at=inv.completed_at,
        duration_ms=inv.duration_ms,
    )


@router.get("/investigation/{investigation_id}/similar")
def get_similar_cases(investigation_id: str, db: Session = Depends(get_db)):
    """Return top-3 similar known misinformation cases using RAG search."""
    try:
        inv_uuid = uuid.UUID(investigation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investigation ID")

    inv = db.query(Investigation).filter(Investigation.id == inv_uuid).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    from app.services.rag_search import search_incidents
    query_parts = [
        inv.summary_en or "",
        inv.actual_origin_country or "",
        inv.actual_origin_city or "",
        str(inv.actual_origin_date or ""),
    ]
    query = " ".join(p for p in query_parts if p).strip()
    if not query:
        return []

    results = search_incidents(db, query, top_k=3)
    return [
        {
            "id": r.get("id"),
            "title_en": r.get("title_en"),
            "title_bn": r.get("title_bn"),
            "false_claim_en": r.get("false_claim_en"),
            "actual_origin_country": r.get("actual_origin_country"),
            "actual_origin_city": r.get("actual_origin_city"),
            "actual_origin_date": str(r.get("actual_origin_date") or ""),
            "debunk_url": r.get("debunk_url"),
            "debunk_source": r.get("debunk_source"),
            "rrf_score": r.get("rrf_score", 0),
        }
        for r in results
    ]


@router.get("/investigation/{investigation_id}/reach")
def get_estimated_reach(investigation_id: str, db: Session = Depends(get_db)):
    """Estimate how many people this misinformation potentially reached."""
    try:
        inv_uuid = uuid.UUID(investigation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid investigation ID")

    inv = db.query(Investigation).filter(Investigation.id == inv_uuid).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Investigation not found")

    # Look up share count from viral_videos if linked
    from app.models import ViralVideo
    viral = db.query(ViralVideo).filter(ViralVideo.investigation_id == inv_uuid).first()
    base_shares = viral.share_count if viral and viral.share_count else 0

    # Bangladesh average: each share reaches ~7 people (friend network effect)
    # Viral threshold multiplier: 500K+ shares = 4x amplification
    network_multiplier = 7
    if base_shares >= 500_000:
        amplification = 4.0
    elif base_shares >= 100_000:
        amplification = 2.5
    elif base_shares >= 10_000:
        amplification = 1.8
    else:
        amplification = 1.2

    estimated = int(base_shares * network_multiplier * amplification) if base_shares else None

    return {
        "base_shares": base_shares,
        "estimated_reach": estimated,
        "network_multiplier": network_multiplier,
        "amplification": amplification,
        "verdict": inv.verdict,
    }
