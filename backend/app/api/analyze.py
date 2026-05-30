import uuid
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from rq import Queue
import redis as redis_lib

from app.deps import get_db, get_redis
from app.config import get_settings
from app.models import Investigation
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.workers.tasks import run_investigation
from app.utils.language import extract_claimed_date

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(
    body: AnalyzeRequest,
    db: Session = Depends(get_db),
    redis: redis_lib.Redis = Depends(get_redis),
):
    if not body.video_url:
        raise HTTPException(status_code=400, detail="video_url is required")

    # Create investigation record
    inv = Investigation(
        video_url=body.video_url,
        claimed_location=body.claimed_context,
        claimed_date=extract_claimed_date(body.claimed_context) if body.claimed_context else None,
        status="queued",
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)

    job_id = str(inv.id)

    # Enqueue investigation job
    q = Queue("investigation_queue", connection=redis)
    q.enqueue(run_investigation, job_id, job_id=job_id, job_timeout=1800)

    return AnalyzeResponse(
        investigation_id=job_id,
        stream_url=f"/api/stream/{job_id}",
        share_url=f"/share/{job_id}",
    )

@router.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_upload(
    video: UploadFile = File(...),
    claimed_context: str = Form(""),
    db: Session = Depends(get_db),
    redis: redis_lib.Redis = Depends(get_redis),
):
    if not video.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    settings = get_settings()
    os.makedirs(settings.videos_dir, exist_ok=True)
    
    # Create investigation record first to get ID
    inv = Investigation(
        video_url="local://upload",  # Temporary
        claimed_location=claimed_context,
        claimed_date=extract_claimed_date(claimed_context) if claimed_context else None,
        status="queued",
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    
    job_id = str(inv.id)
    
    # Save uploaded file
    file_path = os.path.join(settings.videos_dir, f"{job_id}.mp4")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
        
    inv.video_url = f"local://{job_id}.mp4"
    db.commit()
    
    # Enqueue investigation job
    q = Queue("investigation_queue", connection=redis)
    q.enqueue(run_investigation, job_id, job_id=job_id, job_timeout=1800)

    return AnalyzeResponse(
        investigation_id=job_id,
        stream_url=f"/api/stream/{job_id}",
        share_url=f"/share/{job_id}",
    )
