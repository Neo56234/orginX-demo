import logging
import uuid
import os
import concurrent.futures
from datetime import datetime
import redis

from app.config import get_settings
from app.database import SessionLocal
from app.models import Investigation

# Services
from app.services.video_downloader import download_video
from app.services.frame_extractor import extract_frames
from app.services.card_generator import generate_card
from app.services.phash import compute_phash
from app.services.clip_service import get_clip_embedding
from app.models import FrameEmbedding, AgentRun
from app.utils.pubsub import publish_investigation_complete

# Agents
from app.agents.geolocator import GeolocatorAgent
from app.agents.chronologist import ChronologistAgent
from app.agents.tracer import TracerAgent
from app.agents.linguist import LinguistAgent
from app.agents.adjudicator import AdjudicatorAgent

logger = logging.getLogger("originx.tasks")


def run_investigation(investigation_id: str) -> dict:
    """
    Main investigation orchestration task.
    Phase 1: full implementation (download, extract, run 4 agents in parallel, verdict, card).
    """
    settings = get_settings()
    db = SessionLocal()
    redis_client = redis.Redis.from_url(settings.redis_url)
    inv = None

    try:
        inv = db.query(Investigation).filter(
            Investigation.id == uuid.UUID(investigation_id)
        ).first()

        if not inv:
            logger.error("Investigation not found: %s", investigation_id)
            return {"error": "not_found"}

        logger.info("Investigation started — id=%s url=%s", investigation_id, inv.video_url)
        inv.status = "processing"
        db.commit()

        # FAST TRACK: Check if it's a Known Case
        from app.models import KnownCase
        import json
        
        known_case = db.query(KnownCase).filter(KnownCase.debunk_url == inv.video_url).first()
        if known_case:
            logger.info("FAST TRACK: Exact match found in known_cases DB!")
            
            # Emit artificial completion for all agents to update UI
            for agent in ["tracer", "geolocator", "linguist", "chronologist", "adjudicator"]:
                redis_client.publish(f"investigation:{investigation_id}", json.dumps({
                    "agent": agent,
                    "event": "agent_started",
                    "data": {}
                }))
                
            redis_client.publish(f"investigation:{investigation_id}", json.dumps({
                "agent": "tracer",
                "event": "agent_finding",
                "data": {
                    "type": "db_match",
                    "value": f"Exact Match in OriginX DB: {known_case.title_en}",
                    "confidence": 1.0,
                    "description": "Video perfectly matches a previously debunked known case.",
                    "weight": "high",
                }
            }))
            
            for agent in ["tracer", "geolocator", "linguist", "chronologist"]:
                redis_client.publish(f"investigation:{investigation_id}", json.dumps({
                    "agent": agent,
                    "event": "agent_complete",
                    "data": {"status": "fast_tracked"}
                }))

            # Artificial Verdict
            _origin_date = str(known_case.actual_origin_date) if known_case.actual_origin_date else "অজানা তারিখ"
            _origin_city = known_case.actual_origin_city or ""
            _origin_loc = f"{_origin_city}, {known_case.actual_origin_country}" if _origin_city else known_case.actual_origin_country
            verdict = {
                "verdict": "mismatch",
                "confidence": 0.99,
                "summary_bn": f"এই ভিডিওটি '{known_case.title_bn}' — {_origin_date}। দাবি করা প্রসঙ্গ মিথ্যা।",
                "summary_en": f"This video is '{known_case.title_en}' ({_origin_date}). The claimed context is false.",
                "actual_origin": {
                    "country": known_case.actual_origin_country,
                    "city": known_case.actual_origin_city,
                    "earliest_date": _origin_date,
                    "confidence": 0.99,
                },
                "key_evidence": [
                    {"agent": "tracer", "finding": "URL Match — OriginX DB-তে নথিভুক্ত ঘটনার সাথে হুবহু মিলছে", "weight": "high"},
                    {"agent": "chronologist", "finding": f"প্রকৃত তারিখ: {_origin_date} | ঘটনাস্থল: {_origin_loc}", "weight": "high"},
                    {"agent": "adjudicator", "finding": known_case.title_en, "weight": "high"},
                ],
                "card_text": {
                    "headline_bn": "পুরনো ভিডিও — মিথ্যা প্রসঙ্গ",
                    "subheadline_bn": known_case.title_bn,
                    "evidence_snippet_bn": f"এই ভিডিওটি {_origin_date}-এর ঘটনা, আজকের নয়।",
                },
            }
            
            inv.verdict = verdict["verdict"]
            inv.confidence = verdict["confidence"]
            inv.summary_en = verdict["summary_en"]
            inv.summary_bn = verdict["summary_bn"]
            inv.evidence = verdict["key_evidence"]
            inv.status = "complete"
            inv.completed_at = datetime.utcnow()
            started_at_naive = inv.started_at.replace(tzinfo=None) if inv.started_at else inv.completed_at
            inv.duration_ms = int((inv.completed_at - started_at_naive).total_seconds() * 1000)
            db.commit()
            
            publish_investigation_complete(redis_client, investigation_id, verdict)
            
            return {"status": "complete", "fast_track": True, "investigation_id": investigation_id}

        # Activate all agents on the UI immediately so the user sees them start
        import json as _json
        for _agent in ["geolocator", "chronologist", "tracer", "linguist"]:
            redis_client.publish(f"investigation:{investigation_id}", _json.dumps({
                "agent": _agent, "event": "agent_started", "data": {}
            }))

        # Step 1: Download (or resolve local upload)
        logger.info("Downloading video...")
        frames = []
        video_path = None

        if inv.video_url and inv.video_url.startswith("local://"):
            # Uploaded file — resolve directly from disk, no download needed
            filename = inv.video_url[len("local://"):]
            local_path = os.path.join(settings.videos_dir, filename)
            if os.path.exists(local_path):
                video_path = local_path
                logger.info("Local upload resolved: %s", video_path)
            else:
                logger.warning("Local upload file not found: %s", local_path)
        else:
            try:
                video_path = download_video(inv.video_url, investigation_id)
            except Exception as dl_exc:
                logger.warning("Video download failed (%s) — continuing with URL-only analysis", dl_exc)
                redis_client.publish(f"investigation:{investigation_id}", _json.dumps({
                    "agent": "tracer",
                    "event": "agent_finding",
                    "data": {
                        "type": "download_warning",
                        "description": f"Video download blocked ({type(dl_exc).__name__}) — running URL-only analysis",
                        "weight": "low",
                    },
                }))

        # Step 2: Extract frames (only if download succeeded)
        if video_path:
            logger.info("Extracting frames...")
            try:
                frames = extract_frames(video_path, investigation_id) or []
            except Exception as fe_exc:
                logger.warning("Frame extraction failed (%s) — continuing with 0 frames", fe_exc)
            
        import json
        phash_matched_case = None
        prior_investigation_match = None

        if video_path:
            from app.services.chromaprint import extract_fingerprint
            audio_fp = extract_fingerprint(video_path)
            if audio_fp:
                if inv.agent_outputs is None:
                    inv.agent_outputs = {}
                inv.agent_outputs = {**inv.agent_outputs, "audio_fingerprint": audio_fp}
                db.commit()
                _check_audio_match(db, inv, audio_fp["fingerprint"])

            # Step 3: Compute pHash and CLIP for each frame and store in DB
            if frames:
                logger.info("Computing pHash and CLIP for %d frames...", len(frames))
                from app.services.phash import is_duplicate
                from sqlalchemy import or_
                known_cases_with_hash = db.query(KnownCase).filter(
                    or_(KnownCase.sample_phash.isnot(None), KnownCase.sample_phashes.isnot(None))
                ).all()

                # Load prior investigation frame pHashes for cross-investigation dedup
                prior_frames = (
                    db.query(FrameEmbedding, Investigation)
                    .join(Investigation, FrameEmbedding.investigation_id == Investigation.id)
                    .filter(
                        Investigation.id != inv.id,
                        Investigation.status == "complete",
                        Investigation.verdict.isnot(None),
                        FrameEmbedding.phash.isnot(None),
                    )
                    .all()
                )

                for idx, frame_path in enumerate(frames):
                    phash_val = compute_phash(frame_path)
                    clip_emb = get_clip_embedding(frame_path)
                    if phash_val:
                        fe = FrameEmbedding(
                            investigation_id=inv.id,
                            frame_index=idx,
                            frame_path=frame_path,
                            phash=phash_val,
                            clip_embedding=clip_emb,
                        )
                        db.add(fe)

                        if not phash_matched_case:
                            for kc in known_cases_with_hash:
                                if kc.sample_phash and is_duplicate(phash_val, kc.sample_phash):
                                    phash_matched_case = kc
                                    break
                                if kc.sample_phashes:
                                    for kc_phash in kc.sample_phashes:
                                        if kc_phash and is_duplicate(phash_val, kc_phash):
                                            phash_matched_case = kc
                                            break
                                if phash_matched_case:
                                    break

                        # Also check against prior investigation frames
                        if not phash_matched_case and not prior_investigation_match:
                            for prior_fe, prior_inv in prior_frames:
                                if is_duplicate(phash_val, prior_fe.phash):
                                    # Only fast-track if that investigation had a definitive verdict
                                    if prior_inv.verdict in ("mismatch", "authentic") and (prior_inv.confidence or 0) >= 0.7:
                                        prior_investigation_match = prior_inv
                                        logger.info(
                                            "pHash match against prior investigation %s (verdict=%s conf=%.2f)",
                                            prior_inv.id, prior_inv.verdict, prior_inv.confidence,
                                        )
                                    else:
                                        logger.info(
                                            "pHash match found but prior verdict is weak (%s, %.2f) — skipping fast-track",
                                            prior_inv.verdict, prior_inv.confidence or 0,
                                        )
                                    break

                db.commit()
                logger.info("Frame embeddings stored.")

        # FAST TRACK 2: pHash Visual Match against known_cases
        if phash_matched_case:
            logger.info("FAST TRACK: Visual pHash match found in known_cases DB!")
            return _fast_track_complete(db, redis_client, inv, investigation_id, phash_matched_case, match_type="Visual (pHash) Match")

        # FAST TRACK 3: pHash match against a prior investigation
        if prior_investigation_match:
            logger.info("FAST TRACK: pHash match against prior investigation %s", prior_investigation_match.id)
            return _fast_track_prior_investigation(db, redis_client, inv, investigation_id, prior_investigation_match)
            
        # Step 4: Run Agents in Parallel
        context = {
            "video_url": inv.video_url,
            "claimed_context": inv.claimed_location or "No context provided"
        }
        
        agent_outputs = {}
        
        linguist = LinguistAgent(investigation_id, redis_client)
        geolocator = GeolocatorAgent(investigation_id, redis_client)
        chronologist = ChronologistAgent(investigation_id, redis_client)
        tracer = TracerAgent(investigation_id, redis_client)
        
        logger.info("Running parallel agents...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_agent = {
                executor.submit(linguist.run, frames, context): "linguist",
                executor.submit(geolocator.run, frames, context): "geolocator",
                executor.submit(chronologist.run, frames, context): "chronologist",
                executor.submit(tracer.run, frames, context): "tracer"
            }
            for future in concurrent.futures.as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                agent_run = AgentRun(
                    investigation_id=inv.id,
                    agent_name=agent_name,
                )
                try:
                    result = future.result()
                    agent_outputs[agent_name] = result
                    agent_run.status = "complete"
                    agent_run.findings = result
                except Exception as exc:
                    logger.error("%s agent generated an exception: %s", agent_name, exc)
                    agent_outputs[agent_name] = {"error": str(exc)}
                    agent_run.status = "failed"
                    agent_run.error_message = str(exc)
                agent_run.completed_at = datetime.utcnow()
                db.add(agent_run)
            db.commit()
                    
        context["agent_outputs"] = agent_outputs
        inv.agent_outputs = agent_outputs
        db.commit()

        # Step 4: Adjudicate
        logger.info("Running Adjudicator...")
        adjudicator = AdjudicatorAgent(investigation_id, redis_client)
        verdict = adjudicator.run(frames, context)
        
        inv.verdict = verdict.get("verdict", "insufficient_evidence")
        inv.confidence = verdict.get("confidence", 0.0)
        inv.summary_en = verdict.get("summary_en", "")
        inv.summary_bn = verdict.get("summary_bn", "")
        inv.evidence = verdict.get("key_evidence", [])
        
        actual_origin = verdict.get("actual_origin", {})
        if actual_origin:
            inv.actual_origin_country = actual_origin.get("country")
            inv.actual_origin_city = actual_origin.get("city")
            if actual_origin.get("earliest_date"):
                try:
                    inv.actual_origin_date = datetime.strptime(actual_origin["earliest_date"], "%Y-%m-%d").date()
                except ValueError:
                    pass
            inv.actual_origin_confidence = actual_origin.get("confidence")
        
        db.commit()

        from app.services.campaign_detector import detect_campaign
        campaign = detect_campaign(db, inv)
        if campaign:
            logger.info(f"Campaign detected for investigation {inv.id}: {campaign.investigation_count} matching investigations")

        # Step 5: Card Generator
        card_text = verdict.get("card_text")
        if card_text and inv.verdict != "authentic":
            logger.info("Generating counter-narrative card...")
            card_path = generate_card(
                investigation_id,
                card_text.get("headline_bn", "মিথ্যা দাবি"),
                card_text.get("subheadline_bn", ""),
                card_text.get("evidence_snippet_bn", ""),
                thumbnail_url=frames[0] if frames else None
            )
            if card_path:
                inv.counter_card_path = f"/cards/{os.path.basename(card_path)}"
                db.commit()

        # Finalize
        inv.status = "complete"
        inv.completed_at = datetime.utcnow()
        started_at_naive = inv.started_at.replace(tzinfo=None) if inv.started_at else inv.completed_at
        inv.duration_ms = int((inv.completed_at - started_at_naive).total_seconds() * 1000)
        db.commit()

        logger.info("Investigation complete — id=%s", investigation_id)
        
        # Emit complete event to web clients
        publish_investigation_complete(redis_client, investigation_id, verdict)
        
        return {"status": "complete", "investigation_id": investigation_id}

    except Exception as exc:
        logger.exception("Investigation failed — id=%s error=%s", investigation_id, exc)
        if inv:
            inv.status = "failed"
            db.commit()
        return {"error": str(exc)}
    finally:
        db.close()

def _check_audio_match(db, inv, fingerprint: str):
    """Find prior investigations with matching audio fingerprint."""
    from app.services.chromaprint import fingerprints_match
    import redis as redis_lib
    import json
    from app.config import get_settings

    settings = get_settings()
    r = redis_lib.from_url(settings.redis_url)
    channel = f"investigation:{inv.id}"

    from app.models import Investigation

    recent = (
        db.query(Investigation)
        .filter(
            Investigation.id != inv.id,
            Investigation.agent_outputs.isnot(None),
            Investigation.agent_outputs["audio_fingerprint"].isnot(None),
        )
        .limit(50)
        .all()
    )

    matches = []
    for other in recent:
        other_fp = other.agent_outputs.get("audio_fingerprint", {}).get("fingerprint")
        if other_fp and fingerprints_match(fingerprint, other_fp):
            matches.append(str(other.id))

    if matches:
        msg = json.dumps({
            "agent": "tracer",
            "event": "agent_finding",
            "data": {
                "type": "audio_match",
                "value": f"Audio match found in {len(matches)} prior investigation(s)",
                "confidence": 0.92,
                "description": f"Identical audio fingerprint detected. Matched investigation IDs: {', '.join(matches[:3])}",
                "weight": "high",
            },
        })
        r.publish(channel, msg)

def _fast_track_complete(db, redis_client, inv, investigation_id, known_case, match_type="URL Match"):
    import json
    from datetime import datetime
    from app.utils.pubsub import publish_investigation_complete
    
    # Emit artificial completion for all agents to update UI
    for agent in ["tracer", "geolocator", "linguist", "chronologist", "adjudicator"]:
        redis_client.publish(f"investigation:{investigation_id}", json.dumps({
            "agent": agent,
            "event": "agent_started",
            "data": {}
        }))
        
    redis_client.publish(f"investigation:{investigation_id}", json.dumps({
        "agent": "tracer",
        "event": "agent_finding",
        "data": {
            "type": "db_match",
            "value": f"Exact Match in OriginX DB: {known_case.title_bn}",
            "confidence": 1.0,
            "description": f"Video perfectly matches a previously debunked known case via {match_type}.",
            "weight": "high",
        }
    }))
    
    for agent in ["tracer", "geolocator", "linguist", "chronologist"]:
        redis_client.publish(f"investigation:{investigation_id}", json.dumps({
            "agent": agent,
            "event": "agent_complete",
            "data": {"status": "fast_tracked"}
        }))

    origin_date_str = str(known_case.actual_origin_date) if known_case.actual_origin_date else "অজানা তারিখ"
    origin_city = known_case.actual_origin_city or ""
    origin_location = f"{origin_city}, {known_case.actual_origin_country}" if origin_city else known_case.actual_origin_country

    verdict = {
        "verdict": "mismatch",
        "confidence": 0.99,
        "summary_bn": f"এই ভিডিওটি '{known_case.title_bn}' — {origin_date_str}। দাবি করা প্রসঙ্গ মিথ্যা।",
        "summary_en": f"This video is '{known_case.title_en}' ({origin_date_str}). The claimed context is false.",
        "actual_origin": {
            "country": known_case.actual_origin_country,
            "city": known_case.actual_origin_city,
            "earliest_date": origin_date_str,
            "confidence": 0.99,
        },
        "key_evidence": [
            {
                "agent": "tracer",
                "finding": f"{match_type} — ভিডিওটি OriginX DB-তে নথিভুক্ত ঘটনার সাথে হুবহু মিলছে",
                "weight": "high",
            },
            {
                "agent": "chronologist",
                "finding": f"প্রকৃত তারিখ: {origin_date_str} | ঘটনাস্থল: {origin_location}",
                "weight": "high",
            },
            {
                "agent": "adjudicator",
                "finding": known_case.title_en,
                "weight": "high",
            },
        ],
        "actual_origin_date": origin_date_str,
        "card_text": {
            "headline_bn": "পুরনো ভিডিও — মিথ্যা প্রসঙ্গ",
            "subheadline_bn": known_case.title_bn,
            "evidence_snippet_bn": f"এই ভিডিওটি {origin_date_str}-এর ঘটনা, আজকের নয়।",
        },
    }
    
    inv.verdict = verdict["verdict"]
    inv.confidence = verdict["confidence"]
    inv.summary_en = verdict["summary_en"]
    inv.summary_bn = verdict["summary_bn"]
    inv.evidence = verdict["key_evidence"]
    inv.status = "complete"
    inv.completed_at = datetime.utcnow()
    started_at_naive = inv.started_at.replace(tzinfo=None) if inv.started_at else inv.completed_at
    inv.duration_ms = int((inv.completed_at - started_at_naive).total_seconds() * 1000)
    db.commit()
    
    publish_investigation_complete(redis_client, investigation_id, verdict)

    return {"status": "complete", "fast_track": True, "investigation_id": investigation_id}


def _fast_track_prior_investigation(db, redis_client, inv, investigation_id, prior_inv):
    """Fast-track using verdict from a prior investigation with matching pHash frames."""
    import json
    from datetime import datetime
    from app.utils.pubsub import publish_investigation_complete

    for agent in ["tracer", "geolocator", "linguist", "chronologist", "adjudicator"]:
        redis_client.publish(f"investigation:{investigation_id}", json.dumps({
            "agent": agent, "event": "agent_started", "data": {}
        }))

    prior_id_str = str(prior_inv.id)
    prior_verdict = prior_inv.verdict or "insufficient_evidence"
    prior_conf = prior_inv.confidence or 0.5
    prior_summary_en = prior_inv.summary_en or "Duplicate video detected from prior investigation."
    prior_summary_bn = prior_inv.summary_bn or "আগের তদন্তের সাথে হুবহু মিলে যাওয়া ভিডিও সনাক্ত হয়েছে।"
    prior_country = prior_inv.actual_origin_country
    prior_city = prior_inv.actual_origin_city
    prior_date = str(prior_inv.actual_origin_date) if prior_inv.actual_origin_date else None
    prior_evidence = prior_inv.evidence or []

    redis_client.publish(f"investigation:{investigation_id}", json.dumps({
        "agent": "tracer",
        "event": "agent_finding",
        "data": {
            "type": "prior_investigation_match",
            "description": f"Visual pHash match — identical video found in prior investigation (verdict: {prior_verdict.upper()})",
            "weight": "high",
        },
    }))

    for agent in ["tracer", "geolocator", "linguist", "chronologist"]:
        redis_client.publish(f"investigation:{investigation_id}", json.dumps({
            "agent": agent, "event": "agent_complete", "data": {"status": "fast_tracked"}
        }))

    key_evidence = [
        {
            "agent": "tracer",
            "finding": f"Visual pHash match — আগের investigation-এর সাথে হুবহু মিলছে (ID: {prior_id_str[:8]}...)",
            "weight": "high",
        },
        *prior_evidence[:3],
    ]

    verdict = {
        "verdict": prior_verdict,
        "confidence": min(prior_conf, 0.97),
        "summary_bn": prior_summary_bn,
        "summary_en": prior_summary_en,
        "actual_origin": {
            "country": prior_country,
            "city": prior_city,
            "earliest_date": prior_date,
            "confidence": min(prior_conf, 0.97),
        },
        "key_evidence": key_evidence,
    }

    inv.verdict = verdict["verdict"]
    inv.confidence = verdict["confidence"]
    inv.summary_en = verdict["summary_en"]
    inv.summary_bn = verdict["summary_bn"]
    inv.evidence = verdict["key_evidence"]
    inv.actual_origin_country = prior_country
    inv.actual_origin_city = prior_city
    inv.actual_origin_date = prior_inv.actual_origin_date
    inv.status = "complete"
    inv.completed_at = datetime.utcnow()
    started_at_naive = inv.started_at.replace(tzinfo=None) if inv.started_at else inv.completed_at
    inv.duration_ms = int((inv.completed_at - started_at_naive).total_seconds() * 1000)
    db.commit()

    publish_investigation_complete(redis_client, investigation_id, verdict)
    return {"status": "complete", "fast_track": True, "investigation_id": investigation_id}
