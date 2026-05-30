import Link from "next/link";

export const metadata = {
  title: "OriginX — Documentation & Pitch",
  description:
    "OriginX is Bangladesh's Bangla-first misinformation defense platform. Video provenance, RAG fact-checking, virality monitoring, coordinated-campaign detection — all in one bilingual AI system.",
};

const TEAM = [
  {
    name: "Sakibul Hassan Shovon",
    role: "Team Lead, AI Specialist",
    email: "sakibulhassan.shovon@gmail.com",
    initials: "SH",
  },
  {
    name: "Md. Iftekhar Zawad",
    role: "Backend Engineer",
    email: "",
    initials: "IZ",
  },
  {
    name: "Pabak Dev",
    role: "Frontend Developer, System Design",
    email: "",
    initials: "PD",
  },
];

const STATS = [
  { value: "54", label: "Verified incidents seeded" },
  { value: "5", label: "Specialist AI agents" },
  { value: "12", label: "Region-specific CLIP labels" },
  { value: "2-stage", label: "Provenance pipeline" },
];

const TECH_STACK = {
  Backend: [
    "FastAPI",
    "Python 3.11",
    "SQLAlchemy",
    "Pydantic",
    "RQ (Redis Queue)",
    "Alembic",
    "httpx",
    "BeautifulSoup",
  ],
  Database: [
    "PostgreSQL 16",
    "pgvector",
    "Redis 7",
    "tsvector full-text search",
  ],
  "AI / ML": [
    "Groq LLaMA 3.3-70B",
    "OpenCLIP ViT-B/32",
    "YOLOv8 (ultralytics)",
    "EasyOCR (Bengali + Urdu)",
    "sentence-transformers MiniLM-L12-v2",
    "Chromaprint (fpcalc)",
    "imagehash (pHash)",
  ],
  Frontend: [
    "Next.js 14 App Router",
    "React 18",
    "TypeScript",
    "Tailwind CSS",
    "Framer Motion",
    "Zustand",
    "D3.js",
    "Mapbox GL",
  ],
  Infrastructure: [
    "Docker Compose",
    "Railway (backend)",
    "Netlify (frontend)",
    "yt-dlp",
    "ffmpeg",
  ],
};

const AGENTS = [
  {
    name: "Geolocator",
    role: "Where was this filmed?",
    detail:
      "CLIP ViT-B/32 zero-shot classification across 12 region-specific labels + YOLOv8 license-plate detection + OCR of signage.",
  },
  {
    name: "Linguist",
    role: "What scripts and languages are visible?",
    detail:
      "Unicode-range script detection (Bangla / Urdu / Hindi / Arabic) + dual EasyOCR readers + rule-based script→country inference + channel-name watermark scanner.",
  },
  {
    name: "Tracer",
    role: "When did this clip first appear online?",
    detail:
      "Yandex reverse image search (HTML-scraped) + YouTube Data API duplicate search by claimed-context query. Sorts hits by date to surface earliest known appearance.",
  },
  {
    name: "Chronologist",
    role: "Does the claimed date match reality?",
    detail:
      "YouTube upload metadata + OCR of on-screen dates + Wayback Machine availability API. Flags date contradictions as forced-mismatch evidence.",
  },
  {
    name: "Adjudicator",
    role: "What is the final verdict?",
    detail:
      "Groq LLaMA 3.3-70B in JSON mode (temp 0.1). Synthesises all four agents' evidence into {verdict, confidence, rationale, origin}. Deterministic rule layer post-processes for forced verdicts.",
  },
];

const ENDPOINTS = [
  { method: "POST", path: "/investigations", note: "Submit video/URL, returns investigation_id" },
  { method: "GET", path: "/investigations/{id}", note: "Poll current state + findings" },
  { method: "GET", path: "/investigations/{id}/stream", note: "SSE stream of live agent findings" },
  { method: "GET", path: "/investigations/{id}/card", note: "Bilingual counter-narrative card payload" },
  { method: "GET", path: "/dashboard/viral", note: "Paginated viral-video feed (region/category filters)" },
  { method: "GET", path: "/dashboard/stats", note: "Platform-wide counters" },
  { method: "GET", path: "/dashboard/trust-graph", note: "D3 nodes + edges of bad-actor sources" },
  { method: "GET", path: "/dashboard/credibility-leaderboard", note: "Repeat-offender ranking" },
  { method: "GET", path: "/dashboard/campaigns", note: "Active coordinated-cluster alerts" },
  { method: "POST", path: "/chat", note: "One-shot RAG answer" },
  { method: "POST", path: "/chat/stream", note: "SSE streaming RAG response with citations" },
];

const ROADMAP = [
  {
    phase: "Shipped",
    color: "text-truth",
    border: "border-truth/40",
    items: [
      "Two-stage video provenance pipeline (Stage 1 pHash + audio lookup, Stage 2 five-agent investigation)",
      "Bilingual RAG chatbot with BM25 (tsvector) + pgvector + RRF hybrid retrieval",
      "Virality Monitor dashboard with regional + category filters",
      "Coordinated Campaign Detector (N≥3 pHash match within 48-hour window)",
      "Source Trust Graph (D3 force-directed visualisation)",
      "Self-learning verdict cache (cross-investigation pHash fast-tracking)",
      "Server-Sent Events live agent finding stream",
      "54 seeded verified Bangladesh misinformation incidents",
    ],
  },
  {
    phase: "Next (Q3 2026)",
    color: "text-primary",
    border: "border-primary/40",
    items: [
      "Chrome MV3 browser extension — overlay warning badges on Facebook video posts",
      "WhatsApp webhook channel — forwarded-video verification",
      "Expanded incident corpus (500+ verified cases via partnership with Rumour Scanner)",
      "BanglaBERT integration for deeper Bangla NLP",
      "Audio fingerprint matching against known_cases corpus (currently matches prior investigations only)",
    ],
  },
  {
    phase: "Future",
    color: "text-warning",
    border: "border-warning/40",
    items: [
      "Image and audio provenance pipelines (same architecture, different modalities)",
      "Real-time Facebook / Twitter / TikTok content stream ingestion",
      "Federated verification network across Bangladesh / India / Pakistan civic-tech orgs",
      "Election integrity dashboard with constituency-level monitoring",
      "Public API for journalists, fact-checkers, and platforms",
    ],
  },
];

function Section({
  id,
  eyebrow,
  title,
  subtitle,
  children,
  variant = "default",
}: {
  id: string;
  eyebrow?: string;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  variant?: "default" | "alt";
}) {
  return (
    <section
      id={id}
      className={`scroll-mt-24 py-20 px-6 md:px-12 ${
        variant === "alt" ? "bg-card/40" : ""
      }`}
    >
      <div className="max-w-6xl mx-auto">
        {eyebrow && (
          <p className="font-mono text-xs text-primary uppercase tracking-widest mb-3">
            {eyebrow}
          </p>
        )}
        <h2 className="text-3xl md:text-4xl font-sans font-bold text-white mb-3">
          {title}
        </h2>
        {subtitle && (
          <p className="text-gray-400 text-lg max-w-3xl mb-10">{subtitle}</p>
        )}
        <div className={subtitle ? "" : "mt-10"}>{children}</div>
      </div>
    </section>
  );
}

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-background text-foreground">
      {/* Sticky nav */}
      <nav className="sticky top-0 z-50 backdrop-blur-md bg-background/80 border-b border-gray-800">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 md:px-12 py-4">
          <Link href="/" className="font-sans font-black text-xl text-white">
            Origin<span className="text-primary">X</span>
            <span className="ml-2 font-mono text-xs text-gray-500 hidden sm:inline">
              / docs
            </span>
          </Link>
          <div className="hidden md:flex gap-6 text-sm font-mono text-gray-400">
            <a href="#problem" className="hover:text-white transition-colors">
              Problem
            </a>
            <a href="#solution" className="hover:text-white transition-colors">
              Solution
            </a>
            <a href="#architecture" className="hover:text-white transition-colors">
              Architecture
            </a>
            <a href="#api" className="hover:text-white transition-colors">
              API
            </a>
            <a href="#team" className="hover:text-white transition-colors">
              Team
            </a>
          </div>
          <Link
            href="/"
            className="font-mono text-xs text-white bg-primary px-4 py-2 rounded-full hover:opacity-90 transition-opacity"
          >
            Try the demo →
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden py-24 md:py-32 px-6 md:px-12">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/10 rounded-full blur-[160px] pointer-events-none" />
        <div className="max-w-6xl mx-auto relative z-10">
          <p className="font-mono text-xs text-primary uppercase tracking-widest mb-6">
            Infinity AI BuildFest 2026 · Preliminary Submission
          </p>
          <h1 className="text-5xl md:text-7xl font-sans font-black text-transparent bg-clip-text bg-gradient-to-r from-primary via-white to-primary mb-6 leading-tight">
            Every video has a true origin.
            <br />
            We find it.
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mb-10 leading-relaxed">
            OriginX is Bangladesh's Bangla-first misinformation defence platform.
            We pair a self-learning video provenance engine with a bilingual RAG
            chatbot, a live virality monitor, and a coordinated-campaign detector
            — built for the way misinformation actually spreads here:{" "}
            <span className="text-white">
              real footage with fabricated captions
            </span>
            , not deepfakes.
          </p>
          <div className="flex flex-wrap gap-4">
            <a
              href="https://originxv1.netlify.app/"
              target="_blank"
              rel="noreferrer"
              className="px-6 py-3 bg-primary text-white font-mono text-sm rounded-full hover:opacity-90 transition-opacity"
            >
              Live demo →
            </a>
            <a
              href="https://github.com/sakibul-shovon/originX"
              target="_blank"
              rel="noreferrer"
              className="px-6 py-3 bg-card text-white font-mono text-sm rounded-full border border-gray-700 hover:border-primary transition-colors"
            >
              GitHub repo
            </a>
            <a
              href="#solution"
              className="px-6 py-3 text-gray-400 font-mono text-sm rounded-full hover:text-white transition-colors"
            >
              How it works ↓
            </a>
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section className="border-y border-gray-800 bg-card/30 py-12 px-6 md:px-12">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          {STATS.map((s) => (
            <div key={s.label}>
              <p className="text-4xl md:text-5xl font-mono font-bold text-primary mb-2">
                {s.value}
              </p>
              <p className="text-sm text-gray-400">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Problem */}
      <Section
        id="problem"
        eyebrow="The problem"
        title="Bangladesh has a recycled-video problem, not a deepfake problem."
        subtitle="The dominant misinformation pattern is real footage from elsewhere — Pakistan, India, Syria, or older Bangladesh events — reposted with fabricated captions."
      >
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-card border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-alert mb-3">
              CASE: July 2024 quota reform protests
            </p>
            <p className="text-gray-300 leading-relaxed">
              Lahore PTI rally clips ran as "live protest in Bangladesh." 2013
              Hefazat scenes recirculated as "2024 quota movement." Kashmir
              military footage was passed off as Bangladesh Army crackdowns on
              students. Journalists at Rumour Scanner, AFP Bangladesh, and BOOM
              hand-verified clips one at a time — almost always after the damage
              was done.
            </p>
          </div>
          <div className="bg-card border border-gray-800 rounded-2xl p-6 space-y-4">
            <div>
              <p className="font-mono text-xs text-warning mb-1">Structural #1</p>
              <p className="text-gray-300">
                Off-the-shelf English tools (InVID, Google Reverse Image, Snopes)
                don't handle Bangla-script OCR, don't treat Urdu signage as
                evidence of Pakistani origin, don't surface South Asian scene
                cues.
              </p>
            </div>
            <div>
              <p className="font-mono text-xs text-warning mb-1">Structural #2</p>
              <p className="text-gray-300">
                Verification work doesn't accumulate. When Rumour Scanner debunks
                a clip, the lesson stays on a blog post. The same clip resurfaces
                weeks later and someone verifies it from scratch.
              </p>
            </div>
            <div>
              <p className="font-mono text-xs text-warning mb-1">Structural #3</p>
              <p className="text-gray-300">
                Misinformation is in mixed script (Bangla + Urdu / Hindi /
                Arabic). EasyOCR can't mix Bengali and Urdu in one reader pass —
                off-the-shelf pipelines silently lose half the evidence.
              </p>
            </div>
          </div>
        </div>
      </Section>

      {/* Solution */}
      <Section
        id="solution"
        eyebrow="The solution"
        title="Five integrated surfaces. One shared knowledge base."
        subtitle="Every surface shares the same verified-incidents corpus, so a verdict produced anywhere improves the others."
        variant="alt"
      >
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-background border border-primary/30 rounded-2xl p-6 lg:col-span-2 lg:row-span-2">
            <p className="font-mono text-xs text-primary mb-2">A. CORE</p>
            <h3 className="text-2xl font-bold text-white mb-3">
              Video Provenance Engine
            </h3>
            <p className="text-gray-400 mb-4 text-sm leading-relaxed">
              Two-stage pipeline. Stage 1 is a fingerprint lookup (pHash +
              Chromaprint audio) against 54 seeded incidents — known clips return
              a bilingual verdict in seconds with zero LLM cost. Stage 2 is a
              five-agent investigation for unknown clips. Every Stage 2 verdict
              is written back into the knowledge base, so the next upload of the
              same clip hits Stage 1.
            </p>
            <div className="bg-card/60 border border-gray-800 rounded-xl p-4 font-mono text-xs space-y-2">
              <div className="flex items-center gap-3">
                <span className="text-truth">●</span>
                <span className="text-gray-300">
                  Stage 1 — fingerprint lookup, &lt;3 sec on cache hit
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-warning">●</span>
                <span className="text-gray-300">
                  Stage 2 — 5 parallel agents + LLM adjudicator
                </span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-primary">●</span>
                <span className="text-gray-300">
                  Self-learning loop — every verdict cached for the next caller
                </span>
              </div>
            </div>
          </div>
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-2">B. CHATBOT</p>
            <h3 className="text-xl font-bold text-white mb-2">
              RAG Fact-Checker
            </h3>
            <p className="text-sm text-gray-400">
              Bilingual conversational layer. BM25 (tsvector) + pgvector + RRF
              hybrid retrieval. Groq LLaMA 3.3-70B streams answers grounded only
              in retrieved incidents, with clickable citations.
            </p>
          </div>
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-2">C. DASHBOARD</p>
            <h3 className="text-xl font-bold text-white mb-2">
              Virality Monitor
            </h3>
            <p className="text-sm text-gray-400">
              Live feed of suspect viral videos with regional + category filters.
              SSE-pushed updates as investigations complete. Active-campaign
              alert cards surface automatically.
            </p>
          </div>
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-2">D. CAMPAIGNS</p>
            <h3 className="text-xl font-bold text-white mb-2">
              Coordinated Detection
            </h3>
            <p className="text-sm text-gray-400">
              pHash-matched investigations within a 48-hour rolling window. N≥3
              promotes to a Campaign — turning isolated debunks into network
              intelligence.
            </p>
          </div>
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-2">E. TRUST GRAPH</p>
            <h3 className="text-xl font-bold text-white mb-2">
              Source Credibility
            </h3>
            <p className="text-sm text-gray-400">
              Every account, page, or channel that has shared flagged content is
              scored. Bad actors (score &lt; 0.3) render into a D3 force-directed
              graph plus leaderboard.
            </p>
          </div>
        </div>
      </Section>

      {/* How it works — pipeline */}
      <Section
        id="architecture"
        eyebrow="Architecture"
        title="Two-stage pipeline, five specialist agents, one shared knowledge base."
      >
        {/* Stage diagram */}
        <div className="bg-card border border-gray-800 rounded-2xl p-6 md:p-10 mb-10">
          <div className="font-mono text-sm text-gray-300 space-y-6">
            <div>
              <p className="text-primary font-bold mb-3">
                ① UPLOAD → FRAME EXTRACTION → FINGERPRINTS
              </p>
              <div className="pl-6 border-l-2 border-gray-700 space-y-1 text-xs">
                <p>• ffmpeg extracts evenly-spaced keyframes</p>
                <p>• imagehash → pHash array per frame</p>
                <p>• Chromaprint (fpcalc) → audio fingerprint</p>
              </div>
            </div>

            <div>
              <p className="text-truth font-bold mb-3">
                ② STAGE 1 — FINGERPRINT LOOKUP
              </p>
              <div className="pl-6 border-l-2 border-truth/40 space-y-1 text-xs">
                <p>• pHash Hamming distance ≤ 10 bits vs known_cases</p>
                <p>• Audio fingerprint vs prior investigation hashes</p>
                <p>
                  • HIT → bilingual verdict + counter-narrative card in seconds,
                  zero LLM cost
                </p>
                <p>• MISS → enqueue onto RQ worker for Stage 2</p>
              </div>
            </div>

            <div>
              <p className="text-warning font-bold mb-3">
                ③ STAGE 2 — FIVE-AGENT INVESTIGATION
              </p>
              <div className="pl-6 border-l-2 border-warning/40 space-y-1 text-xs">
                <p>• Geolocator + Linguist + Tracer + Chronologist run in parallel</p>
                <p>• Each emits findings over Redis pub/sub → SSE to frontend</p>
                <p>
                  • Adjudicator (Groq LLaMA 3.3-70B, JSON mode, temp 0.1)
                  synthesises evidence
                </p>
                <p>• Deterministic rule layer post-processes for forced verdicts</p>
              </div>
            </div>

            <div>
              <p className="text-primary font-bold mb-3">
                ④ WRITE-BACK — SELF-LEARNING LOOP
              </p>
              <div className="pl-6 border-l-2 border-primary/40 space-y-1 text-xs">
                <p>• Verdict + pHash array + audio fingerprint → known_cases</p>
                <p>
                  • Next upload of the same clip hits Stage 1, returns in seconds
                </p>
                <p>
                  • Verification compounds — repeated misinformation gets cheaper
                  and faster to detect
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Agents grid */}
        <h3 className="text-2xl font-bold text-white mb-6">The five agents</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {AGENTS.map((a) => (
            <div
              key={a.name}
              className="bg-card border border-gray-800 rounded-2xl p-6"
            >
              <p className="font-mono text-xs text-primary mb-2">
                {a.role}
              </p>
              <h4 className="text-lg font-bold text-white mb-3">{a.name}</h4>
              <p className="text-sm text-gray-400 leading-relaxed">{a.detail}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* Tech stack */}
      <Section
        id="stack"
        eyebrow="Technology"
        title="What's actually under the hood."
        variant="alt"
      >
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(TECH_STACK).map(([category, items]) => (
            <div
              key={category}
              className="bg-background border border-gray-800 rounded-2xl p-6"
            >
              <p className="font-mono text-xs text-primary uppercase tracking-widest mb-4">
                {category}
              </p>
              <ul className="space-y-2">
                {items.map((item) => (
                  <li
                    key={item}
                    className="text-sm text-gray-300 flex items-start gap-2"
                  >
                    <span className="text-primary mt-1">▸</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Section>

      {/* AI Layer */}
      <Section
        id="ai-layer"
        eyebrow="AI layer"
        title="One LLM, two roles. Deterministic rules on top."
      >
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="bg-card border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-truth mb-2">VERDICT SYNTHESIS</p>
            <h3 className="text-xl font-bold text-white mb-3">
              Adjudicator — Groq LLaMA 3.3-70B
            </h3>
            <ul className="text-sm text-gray-400 space-y-2">
              <li>• JSON mode, temperature 0.1</li>
              <li>
                • Input: structured evidence package from 4 upstream agents
              </li>
              <li>
                • Output:{" "}
                <code className="text-primary font-mono">
                  {`{verdict, confidence, rationale, origin}`}
                </code>
              </li>
              <li>
                • Deterministic rules post-process (Urdu + BD claim → mismatch,
                date contradiction → mismatch, etc.)
              </li>
            </ul>
          </div>
          <div className="bg-card border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-2">RAG CHATBOT</p>
            <h3 className="text-xl font-bold text-white mb-3">
              Conversational layer — same LLaMA 3.3-70B
            </h3>
            <ul className="text-sm text-gray-400 space-y-2">
              <li>• Streaming mode, temp 0.3, max_tokens 800</li>
              <li>
                • Retrieval: BM25 (tsvector) + pgvector + RRF (k=60) hybrid
              </li>
              <li>
                • System prompt forbids inventing cases — retrieval-only grounded
              </li>
              <li>
                • Bilingual auto-detect, citation required on every reply
              </li>
            </ul>
          </div>
        </div>

        <div className="bg-card border border-gray-800 rounded-2xl p-6">
          <p className="font-mono text-xs text-warning mb-3">
            WHY ONE MODEL ACROSS BOTH SURFACES
          </p>
          <p className="text-gray-300 leading-relaxed">
            Adding a second LLM would have introduced routing complexity for no
            measurable quality gain. LLaMA 3.3-70B handles both structured JSON
            synthesis (verdicts) and grounded conversational RAG (chatbot)
            comfortably. Groq's hosted inference gives sub-second time-to-first-
            token, which matters because the investigation page streams agent
            findings in real time — adding 4–5 seconds of LLM TTFT would break
            the experience.
          </p>
        </div>
      </Section>

      {/* API */}
      <Section
        id="api"
        eyebrow="API"
        title="REST surface. JSON over HTTPS. OpenAPI auto-generated."
        variant="alt"
      >
        <div className="bg-background border border-gray-800 rounded-2xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-card/60 border-b border-gray-800">
              <tr>
                <th className="text-left p-4 font-mono text-xs text-gray-400 uppercase">
                  Method
                </th>
                <th className="text-left p-4 font-mono text-xs text-gray-400 uppercase">
                  Endpoint
                </th>
                <th className="text-left p-4 font-mono text-xs text-gray-400 uppercase">
                  Purpose
                </th>
              </tr>
            </thead>
            <tbody>
              {ENDPOINTS.map((e, i) => (
                <tr
                  key={e.path}
                  className={`border-b border-gray-800 ${
                    i === ENDPOINTS.length - 1 ? "border-b-0" : ""
                  }`}
                >
                  <td className="p-4">
                    <span
                      className={`font-mono text-xs px-2 py-1 rounded ${
                        e.method === "POST"
                          ? "bg-primary/20 text-primary"
                          : "bg-truth/20 text-truth"
                      }`}
                    >
                      {e.method}
                    </span>
                  </td>
                  <td className="p-4 font-mono text-xs text-white">{e.path}</td>
                  <td className="p-4 text-gray-400 text-sm">{e.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>

      {/* Roadmap */}
      <Section
        id="roadmap"
        eyebrow="Roadmap"
        title="Where we are. Where we're going."
      >
        <div className="grid md:grid-cols-3 gap-6">
          {ROADMAP.map((r) => (
            <div
              key={r.phase}
              className={`bg-card border ${r.border} rounded-2xl p-6`}
            >
              <p className={`font-mono text-xs ${r.color} uppercase tracking-widest mb-4`}>
                {r.phase}
              </p>
              <ul className="space-y-3">
                {r.items.map((item) => (
                  <li
                    key={item}
                    className="text-sm text-gray-300 leading-relaxed flex items-start gap-2"
                  >
                    <span className={`${r.color} mt-1`}>▸</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Section>

      {/* Business model */}
      <Section
        id="business"
        eyebrow="Business model"
        title="Public infrastructure first, partnership tier second."
        variant="alt"
      >
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-truth mb-3">FREE TIER</p>
            <h3 className="text-lg font-bold text-white mb-3">
              Always-free public access
            </h3>
            <p className="text-sm text-gray-400">
              Verdict + chatbot + dashboard are free for citizens, journalists,
              and researchers. Misinformation defense is public infrastructure,
              not gatekept.
            </p>
          </div>
          <div className="bg-background border border-primary/30 rounded-2xl p-6">
            <p className="font-mono text-xs text-primary mb-3">PARTNER TIER</p>
            <h3 className="text-lg font-bold text-white mb-3">
              API + priority queue for news orgs
            </h3>
            <p className="text-sm text-gray-400">
              Paid integration for Rumour Scanner, AFP, BOOM, election
              commissions, and platform integrity teams wanting bulk API access,
              priority verdict queue, and custom dashboards.
            </p>
          </div>
          <div className="bg-background border border-gray-800 rounded-2xl p-6">
            <p className="font-mono text-xs text-warning mb-3">R&D</p>
            <h3 className="text-lg font-bold text-white mb-3">
              Grant-funded development
            </h3>
            <p className="text-sm text-gray-400">
              Civic-tech grants (Google News Initiative, Knight Foundation,
              Meedan, Internews) for ongoing model development, corpus expansion,
              and South Asia-wide federation.
            </p>
          </div>
        </div>
      </Section>

      {/* Team */}
      <Section
        id="team"
        eyebrow="Team"
        title="TestCase_Titans"
        subtitle="Three engineers building Bangla-first misinformation defense for the Infinity AI BuildFest 2026."
      >
        <div className="grid md:grid-cols-3 gap-6">
          {TEAM.map((member) => (
            <div
              key={member.name}
              className="bg-card border border-gray-800 rounded-2xl p-6 text-center"
            >
              <div className="w-24 h-24 mx-auto rounded-full bg-gradient-to-br from-primary to-truth flex items-center justify-center mb-4 ring-4 ring-card">
                <span className="font-mono text-2xl font-bold text-white">
                  {member.initials}
                </span>
              </div>
              <h3 className="text-lg font-bold text-white mb-1">
                {member.name}
              </h3>
              <p className="text-sm text-primary font-mono mb-3">
                {member.role}
              </p>
              {member.email && (
                <a
                  href={`mailto:${member.email}`}
                  className="text-xs text-gray-400 hover:text-white transition-colors break-all"
                >
                  {member.email}
                </a>
              )}
            </div>
          ))}
        </div>
      </Section>

      {/* Vision */}
      <Section
        id="vision"
        eyebrow="Vision"
        title="Verification as a public utility for Bangla-speaking civic spaces."
        variant="alt"
      >
        <div className="max-w-3xl">
          <p className="text-xl text-gray-300 leading-relaxed mb-6">
            Every viral clip checkable in seconds. Every verdict compounding in a
            shared knowledge base. Journalists, citizens, and platforms
            inheriting a misinformation defense network that fact-checking alone
            cannot scale.
          </p>
          <p className="text-gray-400 leading-relaxed">
            OriginX starts with video provenance for Bangladesh, but the
            architecture generalises — image provenance, audio provenance, claim
            provenance, federated verification across South Asia. The
            self-learning loop means the system gets stronger every time it is
            used. Build it once. Use it everywhere.
          </p>
        </div>
      </Section>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 px-6 md:px-12">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <p className="font-sans font-black text-xl text-white">
              Origin<span className="text-primary">X</span>
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Every video has a true origin. We find it.
            </p>
          </div>
          <div className="flex flex-wrap gap-6 text-sm font-mono text-gray-400">
            <a
              href="https://originxv1.netlify.app/"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white transition-colors"
            >
              Live demo
            </a>
            <a
              href="https://github.com/sakibul-shovon/originX"
              target="_blank"
              rel="noreferrer"
              className="hover:text-white transition-colors"
            >
              GitHub
            </a>
            <Link href="/dashboard" className="hover:text-white transition-colors">
              Dashboard
            </Link>
            <Link href="/chat" className="hover:text-white transition-colors">
              Chatbot
            </Link>
            <Link href="/cases" className="hover:text-white transition-colors">
              Cases archive
            </Link>
          </div>
        </div>
        <div className="max-w-6xl mx-auto mt-8 pt-8 border-t border-gray-900 text-xs text-gray-600 font-mono">
          Built for the Infinity AI BuildFest 2026 · BRAC University · Dhaka
        </div>
      </footer>
    </main>
  );
}
