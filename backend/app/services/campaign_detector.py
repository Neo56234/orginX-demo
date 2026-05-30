from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models import Investigation, Campaign
import logging

logger = logging.getLogger(__name__)

CAMPAIGN_THRESHOLD = 3    # min investigations with same phash to be a campaign
CAMPAIGN_WINDOW_HOURS = 48


def detect_campaign(db: Session, inv: Investigation) -> Campaign | None:
    """
    After an investigation completes, check if this video's pHash appears
    in multiple recent investigations — indicating a coordinated campaign.
    """
    if not inv.video_phash:
        return None

    cutoff = datetime.now(timezone.utc) - timedelta(hours=CAMPAIGN_WINDOW_HOURS)

    matches = (
        db.query(Investigation)
        .filter(
            Investigation.video_phash == inv.video_phash,
            Investigation.id != inv.id,
            Investigation.started_at >= cutoff,
        )
        .all()
    )

    total = len(matches) + 1  # include current investigation
    if total < CAMPAIGN_THRESHOLD:
        return None

    # Check if campaign already recorded for this phash
    existing = db.query(Campaign).filter(Campaign.phash == inv.video_phash).first()

    all_ids = [str(m.id) for m in matches] + [str(inv.id)]

    if existing:
        existing.investigation_count = total
        existing.investigation_ids = all_ids
        db.commit()
        logger.info(f"Updated campaign {existing.id}: {total} investigations")
        return existing

    campaign = Campaign(
        phash=inv.video_phash,
        investigation_count=total,
        investigation_ids=all_ids,
        sample_claim_bn=inv.summary_bn,
    )
    db.add(campaign)
    db.commit()
    logger.info(f"New campaign detected: phash={inv.video_phash}, count={total}")
    return campaign
