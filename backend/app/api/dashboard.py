from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.deps import get_db
from app.models import ViralVideo, Investigation, SourceCredibility, Campaign
from sqlalchemy import func as sqlfunc

router = APIRouter()


@router.get("/dashboard/viral")
def viral_feed(
    region: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(12, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(ViralVideo)

    if region:
        query = query.filter(ViralVideo.region == region)
    if category:
        query = query.filter(ViralVideo.category == category)

    videos = (
        query.order_by(ViralVideo.detected_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": v.id,
            "video_url": v.video_url,
            "thumbnail_url": v.thumbnail_url,
            "claim_text": v.claim_text,
            "claim_text_bn": v.claim_text_bn,
            "share_count": v.share_count,
            "detected_at": v.detected_at,
            "region": v.region,
            "category": v.category,
            "investigation_id": str(v.investigation_id) if v.investigation_id else None,
            "is_featured": v.is_featured,
        }
        for v in videos
    ]

@router.get("/dashboard/stats")
def dashboard_stats(db: Session = Depends(get_db)):
    total_viral = db.query(ViralVideo).count()
    total_mismatch = db.query(Investigation).filter(
        Investigation.verdict == "mismatch"
    ).count()
    total_authentic = db.query(Investigation).filter(
        Investigation.verdict == "authentic"
    ).count()

    by_region = (
        db.query(ViralVideo.region, sqlfunc.count(ViralVideo.id))
        .group_by(ViralVideo.region)
        .all()
    )
    by_category = (
        db.query(ViralVideo.category, sqlfunc.count(ViralVideo.id))
        .group_by(ViralVideo.category)
        .all()
    )

    return {
        "total_viral": total_viral,
        "total_mismatch": total_mismatch,
        "total_authentic": total_authentic,
        "by_region": {r: c for r, c in by_region if r},
        "by_category": {cat: c for cat, c in by_category if cat},
    }

@router.get("/dashboard/trust-graph")
def trust_graph(db: Session = Depends(get_db)):
    sources = db.query(SourceCredibility).all()

    nodes = [
        {
            "id": s.source_identifier,
            "label": s.display_name,
            "platform": s.platform,
            "credibility_score": s.credibility_score or 0.5,
            "total_shared": s.total_shared or 0,
            "flagged_count": s.flagged_count or 0,
        }
        for s in sources
    ]

    bad_actors = [s for s in sources if (s.credibility_score or 1.0) < 0.3]
    edges = []
    seen = set()
    for i, a in enumerate(bad_actors):
        for b in bad_actors[i + 1 :]:
            key = tuple(sorted([a.source_identifier, b.source_identifier]))
            if key not in seen:
                edges.append({
                    "source": a.source_identifier,
                    "target": b.source_identifier,
                    "weight": max(1, min(a.flagged_count, b.flagged_count) // 20),
                })
                seen.add(key)

    return {"nodes": nodes, "edges": edges}

@router.get("/dashboard/credibility-leaderboard")
def credibility_leaderboard(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """Top unreliable sources ranked by flagged_count / total_shared ratio."""
    sources = (
        db.query(SourceCredibility)
        .filter(SourceCredibility.flagged_count > 0)
        .order_by(SourceCredibility.flagged_count.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": s.id,
            "platform": s.platform,
            "display_name": s.display_name or s.source_identifier,
            "source_identifier": s.source_identifier,
            "total_shared": s.total_shared or 0,
            "flagged_count": s.flagged_count or 0,
            "credibility_score": round(s.credibility_score or 0.5, 2),
            "flag_rate": round((s.flagged_count or 0) / max(s.total_shared or 1, 1) * 100, 1),
            "last_flagged_at": s.last_flagged_at,
        }
        for s in sources
    ]


@router.get("/dashboard/campaigns")
def active_campaigns(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    campaigns = (
        db.query(Campaign)
        .filter(Campaign.is_active == True)
        .order_by(Campaign.investigation_count.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": c.id,
            "phash": c.phash,
            "investigation_count": c.investigation_count,
            "first_seen_at": c.first_seen_at,
            "sample_claim_bn": c.sample_claim_bn,
            "investigation_ids": c.investigation_ids,
        }
        for c in campaigns
    ]
