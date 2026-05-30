# OriginX — BuildFest 2026 Submission

> Every video has a true origin. We find it.

---

## BASICS TAB

### Project Name
```
OriginX
```

### Elevator Pitch (one-liner)
```
Every video has a true origin — OriginX finds it in 20 seconds, work that takes Bangladeshi fact-checkers 7 hours.
```

### Public Summary
```
OriginX is an AI-powered video provenance intelligence platform built for Bangladesh's misinformation crisis. When a clip goes viral with a false caption — "this is Dhaka, yesterday" — OriginX traces where it actually came from.

Five AI agents work in parallel under a single adjudicator. Tracer hunts prior appearances with perceptual hashing and reverse image search. Chronologist pins the earliest known date. Geolocator maps the real location with CLIP zero-shot scene classification. Linguist reads on-screen text across five scripts. Adjudicator — LLaMA 3.3 70B with strict anti-hallucination rules — issues the final verdict.

Around the core sits a full ecosystem: a Bangla Hybrid-RAG chatbot, a real-time viral-misinformation dashboard, and auto-generated counter-cards for journalists. Every verdict is explainable, every claim is cited. This isn't a demo — it's a public weapon.
```

### Problem Statement
```
In Bangladesh, the dominant form of online misinformation isn't deepfakes — it's real videos shared with false context. 52% of all cases. A 2005 San Diego Zoo clip becomes "Dhaka, yesterday." Pakistani news footage becomes "today's attack on Hindus in Bangladesh." Indian flood footage becomes Sylhet.

Bangladeshi fact-checkers take an average of seven hours to verify one such video. In August 2024, four people died because the fact-check arrived too late.

Three groups feel the damage. Everyday users spread misinformation by accident — a forwarded clip from a relative, no tool to check it. Journalists at AFP Bangladesh, Rumor Scanner, and Prothom Alo cannot keep up with the volume. Platforms have no native tools to fight back at scale. The result is a country where the truth arrives after the harm.
```

### Solution Description
```
OriginX is a multi-agent AI system that traces a video's true origin in under twenty seconds.

Five specialist agents run in parallel, supervised by an Adjudicator that synthesizes their evidence into a single verdict with confidence:

• Tracer — perceptual hashing (pHash) plus reverse image search via Yandex and the YouTube Data API. Once a video is caught, it is caught forever.
• Chronologist — extracts and verifies the earliest known timestamp from archives and metadata.
• Geolocator — CLIP ViT-B/32 zero-shot scene classification identifies the real country and city signals (architecture, signage, vegetation).
• Linguist — EasyOCR across five scripts (Bangla, English, Urdu, Hindi, Malayalam) reads every word on screen and flags foreign-language origin.
• Adjudicator — LLaMA 3.3 70B served via Groq, constrained to cite which agent's evidence it relied on. If no agent has high-confidence evidence, the verdict is "insufficient evidence" rather than a guess.

Around the verification core, OriginX ships a complete misinformation-fighting ecosystem:

• Bangla Knowledge-Base chatbot — Hybrid RAG (BM25 over PostgreSQL tsvector + cosine similarity over pgvector with multilingual MiniLM embeddings, fused via Reciprocal Rank Fusion), streaming Bangla answers with citations.
• Viral Misinformation Monitor (/dashboard) — real-time trending fake-video feed, source credibility leaderboard, automatic coordinated-campaign clustering.
• Auto-generated counter-cards — shareable PNG verdicts for journalists to publish back to social media.

The entire pipeline is async on Redis Queue, agents run in a ThreadPoolExecutor, and verdicts stream to the browser via Server-Sent Events. Every conclusion is decomposable back to the exact agent, the exact evidence, and the exact confidence score that produced it.
```

---

## DATA LIFECYCLE & ENGINEERING

### 1. Data Sources
**Check:** Internal (own DB / app data), Public Web (scraping), User Uploads / Bulk Import, Third-party / Partner Data, External APIs (paid/free)

**Specific sources text box:**
```
• Internal: PostgreSQL + pgvector knowledge base — 89+ verified Bangladesh misinformation incidents, agent verdict history, source-credibility scores.
• External APIs: YouTube Data API v3 (origin tracing), Yandex Reverse Image Search (visual matching), Groq Cloud (LLaMA 3.3 70B inference).
• Public web scraping: AFP Bangladesh, Rumor Scanner, Prothom Alo Fact Check, BOOM Bangladesh — for ground-truth fact-check corpus.
• User uploads: video files and URLs submitted via the web UI.
• Partner data: YouTube API for upload-date and channel-origin signals.
```

### 2. Acquisition Methods
**Check:** Web Scrapers, API Pull / SDK integrations, OCR

**Scrapers / crawlers used:**
```
Custom Python scrapers using requests + BeautifulSoup for fact-check site monitoring. yt-dlp for video acquisition from any URL (YouTube, Facebook, direct links). Playwright reserved for JS-heavy sites where requests fails.
```

**MCP servers / connectors for data access:**
```
Groq SDK (LLaMA 3.3 70B inference), google-api-python-client (YouTube Data API v3), direct HTTPS to Yandex reverse-image endpoint.
```

**AI-driven extraction details:**
```
EasyOCR running across five scripts (Bangla, English, Urdu, Hindi, Malayalam). CLIP ViT-B/32 for zero-shot scene classification and country-level geolocation. Perceptual hashing (pHash) for visual fingerprint matching against the known-fake KB. ffmpeg for keyframe extraction at 1fps, capped at 8 frames per video to bound inference cost.
```

### 3. Parsing, Formats & Cleaning
**Check formats:** JSON, CSV, MP4 (Video), JPEG/PNG (Images), HTML, Markdown

**Parsers used:**
```
ffmpeg for video frame and metadata extraction, Pillow (PIL) for image preprocessing, BeautifulSoup for HTML scraping, Pydantic for API request/response validation, yt-dlp for cross-platform video acquisition.
```

**Formatters / converters:**
```
Pandas for tabular handling, Markdown for verdict cards rendered in the frontend, JSON for API output, ffmpeg for frame extraction and thumbnail generation.
```

**Data cleaning & enrichment:**
```
Frame deduplication via perceptual hash similarity. OCR confidence threshold filtering (>0.5) drops noisy reads. Geographic enrichment via CLIP embedding nearest-neighbor lookup against a labelled country/region corpus. Timestamp normalization to UTC across all sources.
```

**Schema validation:**
```
Pydantic models guard every FastAPI endpoint. SQLAlchemy ORM-level constraints enforce database invariants. Groq tool-call responses validated against JSON Schema before reaching the Adjudicator — malformed model output is rejected, not silently parsed.
```

### 4. Storage Targets
**Check:** Relational (PostgreSQL), Vector DB (pgvector), Object Storage (filesystem volume), Cache / KV (Redis)

**Schema design / partitioning / retention notes:**
```
PostgreSQL 16 with the pgvector extension is the single source of truth. Tables hold verification jobs, per-agent results, KB documents with 384-dim multilingual-MiniLM-L12-v2 embeddings, source credibility history, and the viral-monitor feed. Redis backs both the RQ job queue and the SSE pub/sub channels. A Docker-mounted volume (mediadata) holds uploaded videos and extracted keyframes. Retention: video bytes are purged 7 days after verdict; perceptual hashes and verdicts are kept indefinitely so re-uploads are caught instantly.
```

### 5. Visualization (open source preferred)
**Check:** Recharts

**Visualization details:**
```
Recharts powers all dashboard charts — picked over D3 for React-native composability and over Chart.js for better TypeScript ergonomics. Real-time updates use Server-Sent Events; charts re-render on event without polling. The /verify page streams a per-agent timeline (which agent finished, with what confidence, in what order) — users watch the verdict assemble itself.
```

**Dashboards & reports:**
```
/dashboard route — the Viral Misinformation Monitor: trending fake-video feed, source credibility leaderboard, coordinated-campaign cluster bubbles, geographic heat map of false-content origin countries. Reports: auto-generated PNG counter-cards (shareable evidence verdicts) for journalists, plus exportable CSV of the verdict log for fact-check partners.
```

### 6. Insights — AI, ML & Non-AI
**Check:** Classical ML, LLM Inference / RAG over data, Anomaly Detection, Deep Learning, Statistical Analysis

**AI / ML details:**
```
• CLIP ViT-B/32 — zero-shot scene classification for geolocation
• EasyOCR — multilingual OCR across 5 scripts
• LLaMA 3.3 70B (Groq) — verdict synthesis with strict structured output and anti-hallucination guardrails
• multilingual-MiniLM-L12-v2 — 384-dim sentence embeddings for Hybrid RAG
• Perceptual hashing (pHash) — visual fingerprint matching
• Reciprocal Rank Fusion — fuses BM25 and vector-similarity rankings
```

**Non-AI analytics:**
```
Source credibility scoring as a Bayesian posterior over verdict history. Coordinated-campaign detection via temporal-spatial clustering of source posting patterns. Viral-velocity tracking (shares/hour rate-of-change) for trend ranking. PostgreSQL tsvector full-text search providing the BM25 half of Hybrid RAG.
```

**How are insights delivered to users?**
```
• Real-time SSE streaming on /verify — verdict shown agent-by-agent as evidence arrives, not in one final blob
• /chat — Bangla streaming chatbot with inline citations powered by Hybrid RAG
• /dashboard — live-updating viral feed and credibility leaderboards
• Auto-generated PNG counter-cards for journalists to share back to social media
```

### 7. Pipelines & Orchestration

**Orchestration:**
```
FastAPI async handlers fan out work to a ThreadPoolExecutor running the five agents in parallel. Long-running jobs (video download, frame extraction, CLIP/OCR inference) are pushed to Redis Queue (RQ) workers. Docker Compose orchestrates four services: api, worker, postgres, redis.
```

**Scheduling / Triggers:**
```
Fully event-driven. Triggers: web UI submission, direct API call. RQ workers pull jobs FIFO. No cron — every verification starts from a real user signal.
```

**Streaming / Real-time:**
```
Server-Sent Events stream per-agent verdicts the moment each agent finishes. Redis pub/sub channels multiplex the SSE fan-out from worker processes to all connected browsers. The frontend consumes via the native EventSource API — no WebSocket complexity needed.
```

### 8. Outbound — APIs & Distribution

**Outbound APIs:**
```
REST endpoints exposed by FastAPI: POST /verify (submit URL or upload), GET /verify/{job_id} (status), GET /verify/{job_id}/stream (SSE), POST /chat (RAG query), GET /dashboard/feed (viral monitor). Auto-generated OpenAPI 3 docs at /docs. Rate limits via Redis-backed token bucket.
```

**Webhooks & exports:**
```
PNG counter-card generation endpoint for shareable evidence cards. CSV export of verdict log for fact-check partners. Outbound webhooks delivered to subscriber endpoints when high-confidence false-content is detected (planned partner: Election Commission monitoring desk).
```

**Embeddings / model serving:**
```
CLIP and EasyOCR served in-process via PyTorch — no separate inference server, models live in the worker. Groq Cloud handles managed LLaMA 3.3 70B inference. pgvector handles embedding similarity search in-database (no external vector store required).
```

### 9. Open Source Stack
```
Backend: FastAPI, Uvicorn, SQLAlchemy + Alembic, Pydantic, RQ (Redis Queue), PyTorch, EasyOCR, OpenAI CLIP, BeautifulSoup, yt-dlp, ffmpeg
Storage: PostgreSQL 16 + pgvector, Redis 7
Frontend: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Framer Motion, Zustand, Recharts
Infra: Docker, Docker Compose
```

### 10. Quality, Governance & Observability

**Data quality:**
```
Pydantic + SQLAlchemy schema constraints at every boundary. OCR confidence threshold (>0.5) filters noisy reads before they reach the Adjudicator. Every agent verdict carries a confidence score; the Adjudicator weights accordingly and refuses to guess when no agent crosses threshold. A hand-curated gold-standard verification set anchors regression testing.
```

**Privacy & compliance:**
```
No PII stored from uploaded videos — only perceptual hashes and extracted on-screen text. Chat history is session-scoped, not persisted by default. Source attribution preserved for fact-check transparency — every verdict can be defended publicly.
```

**Lineage & observability:**
```
Every verdict stores a full audit trail: job_id, source URL, all five agent outputs with confidence, the LLM prompt and response, the final verdict. Nothing is a black box. Structured logging via Python logging, FastAPI access logs, RQ dashboard for job throughput. Verdicts are reproducible — same input video, same agent versions, same verdict.
```

**LLM cost & performance:**
```
Groq's tokens-per-second pricing keeps a single verification at ~$0.05. Frame extraction capped at 8 keyframes per video to bound CLIP and OCR cost. Cached perceptual-hash lookups short-circuit duplicate verifications instantly — the second time a known fake appears, the verdict is free.
```

### Anything else about your data stack?
```
OriginX is built on a "one verdict, full provenance" principle. Every conclusion the system reaches decomposes back to the specific agent, the specific evidence, and the specific confidence score that drove it. The Adjudicator is constrained to cite which agent's evidence it used; without high-confidence evidence the verdict is "insufficient evidence," not a guess. This is what makes the system shippable to journalists, the Election Commission, and the Press Council — they need explainability they can defend publicly, not vibes.
```

---

## PUBLISH LOCAL ENVIRONMENT TO INTERNET
**Check:** ngrok, Cloudflare Tunnel

**Tunneling usage notes:**
```
ngrok with a reserved subdomain exposes the local FastAPI server for live judge access during the BuildFest demo window — stable subdomain means the demo URL is identical across sessions, no last-minute reconfiguration. Cloudflare Tunnel serves as the always-on backup (no session timeout on the free tier). Production deployment moves to Railway (backend) and Vercel (frontend); tunneling is dev and demo-day only.
```

---

## STILL NEEDED FROM YOU

1. **Domain dropdown** — paste the options. Likely fit for OriginX: *Media & Communication, Civic Tech, Public Safety, Trust & Safety*.
2. **Challenge dropdown** — paste the options.
3. **Other red-badge tabs** — Links, Build Provenance, AI Detail Usage, Team. Screenshot these and I'll draft them too.
4. **Footer-flagged missing fields**: Data AI Provenance, Tooling & E2E, YouTube Video, Demo Link.
