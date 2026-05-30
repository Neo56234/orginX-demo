<div align="center">

# OriginX

### Every video has a true origin. We find it.

**Bangla-first AI misinformation defense platform for Bangladesh.**

[![Status](https://img.shields.io/badge/status-preliminary%20submission-blue?style=flat-square)](https://originxv1.netlify.app/)
[![Built for](https://img.shields.io/badge/built%20for-Infinity%20AI%20BuildFest%202026-3D8BFF?style=flat-square)](https://originxv1.netlify.app/docs)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](#)
[![Next.js](https://img.shields.io/badge/Next.js%2014-000000?style=flat-square&logo=next.js&logoColor=white)](#)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL%20%2B%20pgvector-336791?style=flat-square&logo=postgresql&logoColor=white)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#license)

**[Live Demo](https://originxv1.netlify.app/) · [Documentation](https://originxv1.netlify.app/docs) · [Investigation](https://originxv1.netlify.app/) · [Dashboard](https://originxv1.netlify.app/dashboard) · [Chatbot](https://originxv1.netlify.app/chat)**

</div>

---

## The problem

Bangladesh has a recycled-video problem, not a deepfake problem.

The dominant misinformation pattern is real footage from elsewhere — Pakistan, India, Syria, or older Bangladesh events — reposted with a fabricated caption. During the July 2024 quota reform protests, Lahore PTI rally clips ran as *"live protest in Bangladesh"*, 2013 Hefazat scenes recirculated as *"2024 quota movement"*, and Kashmir military footage was passed off as Bangladesh Army crackdowns.

The current defense is manual, slow, and does not compound. Off-the-shelf English tools (InVID, Google Reverse Image, Snopes) do not handle Bangla-script OCR, do not treat Urdu signage as evidence of Pakistani origin, and do not surface region-specific scene cues for South Asia. Every time the same fake clip resurfaces, a journalist verifies it from scratch.

OriginX is built to fix this.

---

## What OriginX does

A multi-agent AI platform built around video provenance. Five integrated surfaces, all sharing one verified-incidents knowledge base — so a verdict produced anywhere in the system improves the others.

<table>
<tr>
<td width="50%">

### Video Provenance Engine

Two-stage pipeline. **Stage 1** is a fingerprint lookup (pHash + Chromaprint audio fingerprint) against a verified-incidents database of **54 seeded Bangladesh cases**. Known clips return a bilingual verdict in seconds with zero LLM cost. **Stage 2** is a five-agent investigation (Geolocator, Linguist, Tracer, Chronologist, Adjudicator) for unknown clips. Every Stage 2 verdict is written back into the knowledge base.

</td>
<td width="50%">

### RAG Fact-Checking Chatbot

Bilingual conversational layer over the verified-incidents corpus. Hybrid retrieval combines **PostgreSQL tsvector BM25**, **pgvector semantic similarity**, and **Reciprocal Rank Fusion** (k=60). Groq LLaMA 3.3-70B streams answers grounded only in retrieved context, with citations a user can click through to the source debunk.

</td>
</tr>
<tr>
<td width="50%">

### Virality Monitor Dashboard

Live feed of suspect videos circulating across Bangladesh, with regional filters, category filters (politics, religion, communal, protest), platform-wide stats, and Server-Sent Events pushing updates as new investigations complete.

</td>
<td width="50%">

### Coordinated Campaign Detector

Matches new investigation pHashes against existing ones within a 48-hour rolling window. When three or more independent investigations share a pHash, the system promotes the cluster to a Campaign record, surfacing organised inauthentic behaviour.

</td>
</tr>
<tr>
<td colspan="2">

### Source Trust Graph

Every account, page, and channel that has shared flagged content is scored on a credibility metric. Bad actors (score < 0.3) render into a D3 force-directed graph plus a leaderboard, mapping the repeat-offender ecosystem journalists need to see.

</td>
</tr>
</table>

> **The architectural moat is the self-learning loop.** Verification compounds in a shared knowledge base. Misinformation gets cheaper and slower to spread the more OriginX is used.

---

## Quick stats

| | |
|---|---|
| **54** | verified Bangladesh misinformation incidents seeded |
| **5** | specialist AI agents (Geolocator, Linguist, Tracer, Chronologist, Adjudicator) |
| **12** | region-specific CLIP scene labels |
| **2-stage** | provenance pipeline (fingerprint cache → multi-agent investigation) |
| **≤ 10-bit** | pHash Hamming distance threshold for near-duplicate matching |
| **48-hour** | rolling window for coordinated campaign detection |
| **2 languages** | Bangla + English, end-to-end |

---

## How it works

```
   ┌──────────────────────────────────────────────────────────────┐
   │   UPLOAD → FRAME EXTRACTION (ffmpeg) → FINGERPRINTS          │
   │   • imagehash pHash per keyframe                             │
   │   • Chromaprint (fpcalc) audio fingerprint                   │
   └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   STAGE 1 — FINGERPRINT LOOKUP (sub-second)                  │
   │   pHash Hamming ≤ 10  ─┬─ vs known_cases                     │
   │                        └─ vs prior investigations            │
   │   Audio fingerprint matched vs prior investigations          │
   │                                                              │
   │   HIT  → return bilingual verdict + counter-card             │
   │   MISS → enqueue to RQ worker for Stage 2                    │
   └──────────────────────────────────────────────────────────────┘
                              │
                          (on miss)
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   STAGE 2 — FIVE-AGENT INVESTIGATION                         │
   │                                                              │
   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
   │   │  Geolocator  │  │   Linguist   │  │    Tracer    │       │
   │   │  CLIP + YOLO │  │  OCR x2 + ML │  │  Yandex + YT │       │
   │   └──────────────┘  └──────────────┘  └──────────────┘       │
   │   ┌──────────────┐                                           │
   │   │ Chronologist │   ──┐                                     │
   │   │ Wayback + YT │     │                                     │
   │   └──────────────┘     ▼                                     │
   │                  ┌────────────────────────────────────┐      │
   │                  │  Adjudicator (Groq LLaMA 3.3-70B)  │      │
   │                  │  JSON mode, temp 0.1, +rule layer  │      │
   │                  └────────────────────────────────────┘      │
   └──────────────────────────────────────────────────────────────┘
                              │
                              ▼
   ┌──────────────────────────────────────────────────────────────┐
   │   WRITE-BACK → SELF-LEARNING LOOP                            │
   │   Verdict + pHash array + audio fingerprint → known_cases    │
   │   Next upload of the same clip hits Stage 1 in seconds       │
   └──────────────────────────────────────────────────────────────┘
```

---

## The five agents

| Agent | Question it answers | How |
|-------|---------------------|-----|
| **Geolocator** | Where was this filmed? | CLIP ViT-B/32 zero-shot classification across 12 region-specific labels (Bangladesh / Pakistan / India scenes, Lahore vs Dhaka crowds, regional architecture) + YOLOv8 license-plate detection + OCR of signage |
| **Linguist** | What scripts and languages are visible? | Unicode-range script detection (Bangla / Urdu / Hindi / Arabic) + dual-pass EasyOCR (Bengali+English and Urdu+English readers run separately) + rule-based script→country inference + channel-name watermark scanner |
| **Tracer** | When did this clip first appear online? | Yandex reverse image search on a mid-video keyframe (HTML-scraped) + YouTube Data API duplicate search by claimed-context query. Sorts hits by date to surface earliest known appearance |
| **Chronologist** | Does the claimed date match reality? | YouTube upload metadata + OCR of on-screen date stamps + Wayback Machine availability API. Flags date contradictions as forced-mismatch evidence |
| **Adjudicator** | What is the final verdict? | Groq LLaMA 3.3-70B in JSON mode (temp 0.1). Synthesises the four upstream agents' evidence into `{verdict, confidence, rationale, origin}`. Deterministic rule layer post-processes for forced verdicts |

---

## Tech stack

<table>
<tr>
<td valign="top" width="33%">

**Backend**
- FastAPI · SQLAlchemy · Pydantic
- RQ (Redis Queue) · Alembic
- httpx · BeautifulSoup
- Python 3.11

**Database**
- PostgreSQL 16 + pgvector
- tsvector full-text search
- Redis 7 (queue + pub/sub)

</td>
<td valign="top" width="33%">

**AI / ML**
- Groq LLaMA 3.3-70B
- OpenCLIP ViT-B/32
- YOLOv8 (ultralytics)
- EasyOCR (Bengali + Urdu)
- sentence-transformers
- Chromaprint (fpcalc)
- imagehash

</td>
<td valign="top" width="33%">

**Frontend & Infra**
- Next.js 14 (App Router)
- React 18 · TypeScript
- Tailwind CSS · Framer Motion
- Zustand · D3.js · Mapbox GL
- Docker Compose
- Railway (backend)
- Netlify (frontend)

</td>
</tr>
</table>

---

## Quick start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend dev)
- A Groq API key — get one free at [console.groq.com](https://console.groq.com)
- A YouTube Data API key — for the Tracer + Chronologist agents

### Environment variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_key_here
YOUTUBE_API_KEY=your_youtube_data_api_key
DATABASE_URL=postgresql://originx:originx@postgres:5432/originx
REDIS_URL=redis://redis:6379/0
```

### Run the backend (Docker Compose)

```bash
cd originx
docker-compose up --build
```

This brings up four services:
- `postgres` — PostgreSQL 16 + pgvector
- `redis` — Redis 7
- `api` — FastAPI server at http://localhost:8000
- `worker` — RQ worker for the five-agent pipeline

### Seed the verified-incidents corpus

```bash
docker-compose exec worker python seed_incidents.py
docker-compose exec worker python seed_july_videos.py
docker-compose exec worker python seed_trust_graph.py
docker-compose exec worker python seed_viral.py
```

### Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## Project structure

```
originx/
├── backend/
│   ├── app/
│   │   ├── agents/           # 5 specialist agents
│   │   │   ├── base.py       # BaseAgent lifecycle (emit_started, emit_finding, ...)
│   │   │   ├── geolocator.py # CLIP + YOLO + OCR
│   │   │   ├── linguist.py   # script detection + dual OCR
│   │   │   ├── tracer.py     # Yandex + YouTube Data API
│   │   │   ├── chronologist.py # Wayback + date metadata
│   │   │   └── adjudicator.py  # LLM verdict synthesis
│   │   ├── api/              # FastAPI routes
│   │   │   ├── analyze.py
│   │   │   ├── cases.py
│   │   │   ├── chat.py       # streaming RAG endpoint
│   │   │   ├── dashboard.py
│   │   │   ├── investigation.py
│   │   │   ├── stream.py     # SSE
│   │   │   └── whatsapp.py
│   │   ├── services/         # cross-cutting utilities
│   │   │   ├── campaign_detector.py
│   │   │   ├── chromaprint.py
│   │   │   ├── clip_service.py
│   │   │   ├── frame_extractor.py
│   │   │   ├── llm_client.py
│   │   │   ├── ocr.py
│   │   │   ├── phash.py
│   │   │   ├── rag_search.py   # BM25 + pgvector + RRF
│   │   │   ├── reverse_search.py
│   │   │   ├── wayback.py
│   │   │   ├── yolo_service.py
│   │   │   └── youtube_api.py
│   │   ├── workers/          # RQ task orchestration
│   │   │   └── tasks.py
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── database.py
│   │   ├── config.py
│   │   └── main.py
│   ├── migrations/           # Alembic migrations
│   ├── seed_*.py             # corpus seeders
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx          # Home / upload UI
│   │   ├── dashboard/        # Virality Monitor + Trust Graph
│   │   ├── investigation/    # Live verdict streaming page
│   │   ├── chat/             # Bilingual RAG chatbot
│   │   ├── cases/            # Verified-incidents archive
│   │   ├── share/            # Counter-narrative card pages
│   │   └── docs/             # Pitch deck + tech docs (this is the /docs route)
│   ├── components/
│   │   ├── console/
│   │   ├── dashboard/
│   │   └── share/
│   ├── lib/                  # State + i18n + demo data
│   └── styles/
│
├── extension/                # Chrome MV3 browser extension (roadmap)
└── docker-compose.yml
```

---

## API

REST surface, JSON over HTTPS. OpenAPI auto-generated at `/docs` (the FastAPI one, distinct from the frontend `/docs` page).

### Investigation

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/investigations` | Submit video file or URL, returns `investigation_id` |
| `GET` | `/investigations/{id}` | Poll current state and findings |
| `GET` | `/investigations/{id}/stream` | Server-Sent Events stream of live agent findings |
| `GET` | `/investigations/{id}/card` | Bilingual counter-narrative card payload |

### Dashboard

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/dashboard/viral` | Paginated viral-video feed (region / category filters) |
| `GET` | `/dashboard/stats` | Platform-wide counters |
| `GET` | `/dashboard/trust-graph` | D3 nodes + edges of bad-actor sources |
| `GET` | `/dashboard/credibility-leaderboard` | Repeat-offender ranking |
| `GET` | `/dashboard/campaigns` | Active coordinated-cluster alerts |

### Chatbot

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/chat` | One-shot RAG answer |
| `POST` | `/chat/stream` | SSE streaming RAG response with cited incidents |

---

## What we're proud of

- **One LLM, two roles.** The same LLaMA 3.3-70B serves both the Adjudicator (structured JSON verdict) and the chatbot (streaming bilingual RAG). One prompt-maintenance surface.
- **Deterministic rules on top of the LLM.** Verdicts pass through a small rule layer (Urdu + Bangladesh claim → forced mismatch, date contradiction → forced mismatch). Keeps high-confidence cases pinned to deterministic logic, uses the LLM only for the ambiguous middle.
- **Self-learning verification loop.** Every Stage 2 verdict is written back into the corpus with its pHash array and audio fingerprint. The next upload of the same clip is a sub-second cache hit. Verification compounds.
- **Bilingual end to end.** Bangla + English in OCR, retrieval, generation, output. No translation layer.

---

## Roadmap

**Next (Q3 2026)**
- Chrome MV3 browser extension overlaying warning badges on Facebook video posts
- WhatsApp webhook channel for forwarded-video verification
- Expanded incident corpus (500+ cases) via partnership with Rumour Scanner
- BanglaBERT integration for deeper Bangla NLP
- Audio fingerprint matching against the full known_cases corpus

**Future**
- Image and audio provenance pipelines (same architecture, different modalities)
- Real-time Facebook / Twitter / TikTok content stream ingestion
- Federated verification network across Bangladesh / India / Pakistan civic-tech orgs
- Election integrity dashboard with constituency-level monitoring
- Public API for journalists, fact-checkers, and platforms

---

## Team — TestCase_Titans

| Member | Role |
|---|---|
| **Sakibul Hassan Shovon** | Team Lead, AI Specialist |
| **Md. Iftekhar Zawad** | Backend Engineer |
| **Pabak Dev** | Frontend Developer, System Design |

Built for the **Infinity AI BuildFest 2026** at BRAC University, Dhaka.

---

## Acknowledgments

- **Rumour Scanner Bangladesh**, **AFP Fact Check**, **Alt News** — the human fact-checkers whose verified debunks form the seed corpus and inspire this work.
- **Groq** for fast hosted LLaMA 3.3-70B inference.
- **Hugging Face** for OpenCLIP, Transformers, and sentence-transformers.
- **The Bangladeshi journalism community** for fighting misinformation on a manual, exhausting beat that should not have to be manual or exhausting.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

**OriginX**

*Every video has a true origin. We find it.*

[Live Demo](https://originxv1.netlify.app/) · [Documentation](https://originxv1.netlify.app/docs) · [Report a Bug](https://github.com/sakibul-shovon/originX/issues)

</div>
