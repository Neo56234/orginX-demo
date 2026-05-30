import logging
import asyncio
import httpx
from fastapi import APIRouter, Form, Depends, BackgroundTasks
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import redis as redis_lib
from rq import Queue

from app.deps import get_db, get_redis
from app.models import Investigation
from app.workers.tasks import run_investigation
from app.config import get_settings
from app.database import SessionLocal

logger = logging.getLogger("originx.whatsapp")
router = APIRouter()

async def poll_and_reply(inv_id: str, to_number: str):
    settings = get_settings()
    
    completed = False
    verdict_text = ""
    status = ""
    
    # Poll for max 90s (18 * 5s)
    for _ in range(18):
        await asyncio.sleep(5)
        with SessionLocal() as db:
            inv = db.query(Investigation).filter(Investigation.id == inv_id).first()
            if not inv:
                break
                
            if inv.status in ["complete", "failed"]:
                completed = True
                status = inv.status
                if inv.verdict:
                    is_mismatch = inv.verdict == "mismatch"
                    verdict_text = (
                        f"*[OriginX - তদন্ত সম্পন্ন]*\n\n"
                        f"{'⚠️ *মিথ্যা প্রসঙ্গ সনাক্ত*' if is_mismatch else '✓ *সত্যতা নিশ্চিত*'}\n\n"
                        f"{inv.summary_bn}\n\n"
                        f"বিস্তারিত দেখতে ভিজিট করুন:\n"
                        f"https://originx.ai/investigation/{inv.id}"
                    )
                break
                
    if not completed:
        verdict_text = "দুঃখিত, তদন্ত সম্পন্ন করতে অতিরিক্ত সময় লাগছে। দয়া করে ওয়েবসাইট চেক করুন।"
    elif status == "failed":
        verdict_text = "দুঃখিত, ভিডিওটি বিশ্লেষণ করতে সমস্যা হয়েছে।"

    # Send via Twilio API
    if settings.twilio_account_sid and settings.twilio_auth_token:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json"
        
        data = {
            "From": settings.twilio_whatsapp_from,
            "To": to_number,
            "Body": verdict_text
        }
        
        # If completed successfully, attach the generated counter-card image
        if completed and status == "complete":
            data["MediaUrl"] = f"https://originx.ai/api/cards/{inv_id}.png"
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url,
                    data=data,
                    auth=(settings.twilio_account_sid, settings.twilio_auth_token)
                )
                if resp.status_code >= 400:
                    logger.error("Twilio API Error: %s", resp.text)
                else:
                    logger.info("WhatsApp reply sent to %s", to_number)
        except Exception as e:
            logger.error("Failed to send WhatsApp message: %s", e)


@router.post("/whatsapp/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    MediaUrl0: str = Form(""),
    From: str = Form(""),
    db: Session = Depends(get_db),
    redis: redis_lib.Redis = Depends(get_redis),
):
    """
    Twilio WhatsApp sandbox webhook.
    User forwards a video URL → OriginX returns verdict.
    """
    video_url = MediaUrl0 or Body.strip()

    if not video_url:
        return "OriginX: কোনো ভিডিও URL পাওয়া যায়নি। একটি ভিডিও লিংক পাঠান।"

    logger.info("WhatsApp message from=%s url=%s", From, video_url)

    inv = Investigation(video_url=video_url, status="queued")
    db.add(inv)
    db.commit()
    db.refresh(inv)

    q = Queue("investigation_queue", connection=redis)
    q.enqueue(run_investigation, str(inv.id), job_id=str(inv.id), job_timeout=1800)

    # Poll and reply asynchronously
    background_tasks.add_task(poll_and_reply, str(inv.id), From)

    return (
        f"OriginX অনুসন্ধান শুরু হয়েছে।\n"
        f"ID: {str(inv.id)[:8]}\n"
        f"দয়া করে ১-২ মিনিট অপেক্ষা করুন।"
    )
