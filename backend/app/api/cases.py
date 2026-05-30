from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.deps import get_db
from app.models import KnownCase
from app.schemas import KnownCaseOut

router = APIRouter()


@router.get("/cases", response_model=list[KnownCaseOut])
def list_cases(
    q: Optional[str] = Query(None, description="Search by keyword"),
    country: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = db.query(KnownCase)

    if q:
        search = f"%{q}%"
        query = query.filter(
            KnownCase.title_en.ilike(search)
            | KnownCase.title_bn.ilike(search)
            | KnownCase.false_claim_en.ilike(search)
        )

    if country:
        query = query.filter(KnownCase.actual_origin_country == country)

    if source:
        query = query.filter(KnownCase.debunk_source == source)

    cases = query.order_by(KnownCase.id.desc()).offset(offset).limit(limit).all()
    return [
        KnownCaseOut(
            id=c.id,
            title_bn=c.title_bn,
            title_en=c.title_en,
            false_claim_bn=c.false_claim_bn,
            false_claim_en=c.false_claim_en,
            actual_origin_country=c.actual_origin_country,
            actual_origin_city=c.actual_origin_city,
            actual_origin_date=c.actual_origin_date,
            debunk_url=c.debunk_url,
            debunk_source=c.debunk_source,
        )
        for c in cases
    ]
