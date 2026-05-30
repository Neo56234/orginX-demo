# OriginX — 3-Minute Demo Video Script

**Hackathon:** Infinity AI BuildFest 2026, BRAC University
**Track:** Track 5 — Social Media (InfoTech) — AI for Authenticity, Trust & Information Integrity
**Duration:** 3:00 total

---

## STRUCTURE OVERVIEW

| Time      | Segment                                | Goal                                |
|-----------|----------------------------------------|-------------------------------------|
| 0:00–0:25 | The Problem (Bangladesh context)       | Emotional hook, urgency             |
| 0:25–0:40 | The Solution intro                     | Position OriginX                    |
| 0:40–1:40 | LIVE Demo — 3 video tests              | Prove it works                      |
| 1:40–2:20 | Agent architecture deep dive           | Show the AI                         |
| 2:20–2:45 | Other features (RAG chatbot, etc.)     | Show ecosystem depth                |
| 2:45–3:00 | Closing — vision + ask                 | Land the message                    |

---

## SEGMENT 1 — THE PROBLEM (0:00–0:25)

**Visual:** Quick montage — Facebook screenshots of viral fake news posts. Bengali captions, red overlay text "ভুয়া." "Old Pakistani riot video — shared as Bangladesh Hindu attack." "2013 Shapla Square footage — captioned as 2024 student protest." Numbers ticking up: "10K shares ... 50K shares ... 200K shares."

**Narration (Bangla, urgent tone):**

> "২০২৪-এর আগস্ট। শেখ হাসিনার বিদায়ের পর বাংলাদেশে এক সপ্তাহে ২০০-র বেশি সাম্প্রদায়িক হিংসার ভিডিও viral হয়। বেশিরভাগই — পাকিস্তান, ভারত, কিংবা পুরনো ফুটেজ।
>
> ফলাফল? গুজবের আগুনে নিরীহ মানুষের প্রাণ যায়, ধর্মীয় সম্প্রদায়ের মধ্যে বিভাজন বাড়ে।
>
> Fact-checker-রা ১টা ভিডিও verify করতে ৬-৮ ঘণ্টা সময় নেয়। ততক্ষণে ভিডিওটা ১০ লক্ষ মানুষের কাছে পৌঁছে যায়।
>
> এই যুদ্ধে আমরা হেরে যাচ্ছি।"

**Cut to black. 1 second pause. White text appears:**
> *"আমরা ভাবলাম — যদি AI ৩০ সেকেন্ডে এই কাজটা করতে পারে?"*

---

## SEGMENT 2 — THE SOLUTION (0:25–0:40)

**Visual:** OriginX logo animates in. Tagline appears: *"Every video has a true origin. We find it."*

**Narration (confident, slower):**

> "এটাই OriginX —
> ৫টা specialist AI agent মিলে যেকোনো viral ভিডিওর আসল উৎস, তারিখ, আর প্রসঙ্গ বের করে দেয়।
>
> বাংলা, ইংরেজি — দুটো ভাষাতেই।
> ২৪ সেকেন্ডে।
>
> আজ আমরা তিন ধরনের ভিডিও দিয়ে এটা প্রমাণ করব।"

**[Visual: Show the OriginX homepage at localhost:3000 — clean, dark UI, URL input box prominently displayed]**

---

## SEGMENT 3 — LIVE DEMO (0:40–1:40)

### Demo 1 — pHash Fast-Track (0:40–0:55) — *"The Memory Test"*

**Visual:** Drag-and-drop the "Me at the zoo" video file onto OriginX. Type claim: *"এটা গতকাল ঢাকার মিরপুর চিড়িয়াখানার ভিডিও"*. Click Analyze.

**[On screen: All 5 agent cards instantly turn green ✓ — within 3 seconds]**

**[Verdict modal slides up: 99% MISMATCH — "এই ভিডিওটি 'Me at the zoo' — 2005-04-23, San Diego, USA"]**

**Narration (energetic):**

> "প্রথম video — দাবি করা হলো এটা গতকাল মিরপুর চিড়িয়াখানার ফুটেজ। বাস্তবে এটা ২০০৫ সালের YouTube-এর প্রথম ভিডিও।
>
> দেখুন — **৩ সেকেন্ডে verdict।** ৯৯% confidence।
>
> এটা কীভাবে সম্ভব? OriginX-এর pHash memory। আগে দেখা প্রত্যেকটা ভিডিওর perceptual fingerprint আমাদের database-এ stored। নতুন ভিডিও এলে — Hamming distance দিয়ে instant match। YouTube-এর full investigation চালানোর দরকার নেই।"

**[Wow moment: Highlight the "Visual (pHash) Match" finding on screen]**

---

### Demo 2 — Full Pipeline (0:55–1:20) — *"The Real Investigation"*

**Visual:** Submit a brand new YouTube URL — e.g., a real Pakistani/Indian news video being passed as Bangladesh content. Type claim: *"বাংলাদেশে আজ হিন্দু সম্প্রদায়ের উপর হামলার ভিডিও"*. Click Analyze.

**[All 5 agent cards animate to "RUNNING" status. Live feed scrolls past — each agent emitting findings in real-time]**

**Narration:**

> "দ্বিতীয় video — database-এ নেই। এবার সব ৫টা agent parallel-এ কাজ শুরু করবে।
>
> দেখুন — live thinking। প্রত্যেকটা agent কী খুঁজছে, কী পাচ্ছে, সব real-time-এ visible।"

**[Pause for ~10 seconds — let viewer watch the live feed. Findings appearing:]**
- **🌍 Geolocator:** "Frame 3/6: CLIP → 'Pakistan urban street' (87% confidence)"
- **🗣️ Linguist:** "Frame 2/6: Urdu script detected in on-screen text"
- **🕐 Chronologist:** "Wayback Machine: archived 2023-08-15"
- **🔍 Tracer:** "YouTube duplicate: 'ARY News Pakistan' — published 2023-08-14"
- **⚖️ Adjudicator:** "Synthesizing evidence from specialist agents..."

**[Final verdict slides up: MISMATCH 95% — "Pakistani news video, August 2023"]**

**Narration continues:**

> "৫ এজেন্ট মিলে — ২৪ সেকেন্ডে — আসল উৎস বের। Urdu script detect হয়েছে। CLIP দেখেছে এটা পাকিস্তানি urban setting। YouTube-এ একই ভিডিও ২০২৩ সালের আগস্টে published।
>
> Adjudicator সব evidence ওজন করে decision নিল।"

---

### Demo 3 — URL-Only Analysis (1:20–1:40) — *"The Hard Case"*

**Visual:** Paste a YouTube link that yt-dlp can't download (e.g., age-restricted or blocked). Type claim. Click Analyze.

**[Tracer emits: "Video download blocked — running URL-only analysis." But agents still complete with whatever metadata they can find via YouTube API + Wayback.]**

**Narration:**

> "তৃতীয় test — YouTube এই link block করেছে। ভিডিও download হলো না।
>
> কিন্তু OriginX গ্রাহক করল না। URL metadata, channel info, Wayback archive — যা পেল তা দিয়ে best-effort analysis। **Graceful degradation।** Production-grade system এভাবেই behave করে।"

**[Verdict appears with appropriate confidence level — could be 'insufficient_evidence' with reasoning shown]**

---

## SEGMENT 4 — AGENT ARCHITECTURE DEEP DIVE (1:40–2:20)

**Visual:** Switch to architecture diagram — 5 agent cards arranged in a hexagon around a central "Adjudicator" node. Animated data flow lines.

**Narration (technical confidence):**

> "এই ৫ agent — প্রত্যেকটা একটা specialized AI।"

**[Each agent highlights as it's mentioned — visual focus]**

**🔍 TRACER (blue card):**
> "**Tracer** — কোথায় কোথায় এই ভিডিও আগে দেখা গেছে। Yandex reverse image search, YouTube Data API, আর আমাদের local pHash database — তিন source-এ duplicate খোঁজে।"

**🕐 CHRONOLOGIST (purple card):**
> "**Chronologist** — কখন প্রথম এই ভিডিও online এসেছে। Wayback Machine CDX API দিয়ে web archive, YouTube publication date — earliest evidence খোঁজে।"

**🌍 GEOLOCATOR (green card):**
> "**Geolocator** — ভিডিও কোথায় তোলা। OpenAI-এর CLIP model দিয়ে zero-shot scene classification — ১২টা region-এর মধ্যে কোনটা। সাথে Bangladeshi/Pakistani/Indian news channel name detection।"

**🗣️ LINGUIST (yellow card):**
> "**Linguist** — frame-এ লেখা সব text পড়ে। EasyOCR multi-script — বাংলা, হিন্দি, উর্দু, আরবি, ইংরেজি। উর্দু script detect হলে — সেটা Bangladesh-এর ভিডিও না, এটা strong signal।"

**⚖️ ADJUDICATOR (red card, glowing):**
> "**Adjudicator** — চারজনের evidence সংগ্রহ করে। Groq-এ LLaMA 3.3 70B model call করে। Chain-of-thought reasoning দিয়ে final verdict।
>
> এবং সবচেয়ে important — কেন এই decision নিল, প্রত্যেকটা evidence-এর weight সহ user-কে দেখায়। AI black-box না।"

**[Show "Why this decision?" panel zoomed in — agent badges, weight bars, confidence percentage]**

**Pipeline visualization (5 seconds):**
> "পুরো pipeline — FastAPI backend, Redis queue, parallel ThreadPoolExecutor, Server-Sent Events দিয়ে real-time streaming। PostgreSQL + pgvector + pg_trgm extensions।"

---

## SEGMENT 5 — OTHER FEATURES (2:20–2:45)

**Visual:** Quick cuts through 4 features — each ~5 seconds on screen.

### 5a — RAG-Powered Chatbot (Knowledge Base)

**[Navigate to /chat. Type a question in Bangla: "২০২৪-এর শাপলা চত্বরের ঘটনা সম্পর্কে কী জানো?"]**

**[Streaming answer appears with cited incidents]**

**Narration:**

> "OriginX Knowledge Base — Bangladesh-এর সব verified misinformation case জিজ্ঞেস করতে পারো।
>
> Architecture-এ — **Hybrid RAG**: BM25 full-text search PostgreSQL tsvector-এ, semantic vector search pgvector cosine similarity-তে, আর **Reciprocal Rank Fusion** দুটো result merge করে। Multilingual MiniLM model দিয়ে Bangla-English embedding।
>
> LLM hallucinate করতে পারবে না — শুধু retrieve করা cases থেকেই answer।"

### 5b — Viral Monitor Dashboard

**[Cut to /dashboard. Show: trending viral videos, source credibility leaderboard, campaign detector]**

**Narration:**

> "Viral Monitor — কোন source বারবার ভুয়া ছড়াচ্ছে, কোন ভিডিও coordinated campaign হিসেবে multiple accounts থেকে spread হচ্ছে — সব track।"

### 5c — Counter-Narrative Card Generator

**[Show a generated shareable PNG counter-card in Bangla — ready to post on Facebook]**

**Narration:**

> "Mismatch detect হলে — automatically একটা Bangla counter-card generate হয়। User এক click-এ share করতে পারে। Misinformation-এর বিরুদ্ধে instant rebuttal।"

### 5d — WhatsApp Bot

**[Show WhatsApp screenshot — user forwards a video link, gets verdict back]**

**Narration:**

> "Non-technical users-এর জন্য — WhatsApp bot। যেকোনো ভিডিও link forward করো, ৩০ সেকেন্ডে Bangla verdict ফিরে আসবে।"

---

## SEGMENT 6 — CLOSING (2:45–3:00)

**Visual:** Slow zoom on the OriginX logo. Background — multiple shareable counter-cards floating, each one a "debunked" stamp.

**Narration (calm, deliberate):**

> "গুজবের বিরুদ্ধে যুদ্ধে সময়ই সবচেয়ে বড় অস্ত্র।
>
> OriginX — fact-checker-দের ৮ ঘণ্টার কাজ ৩০ সেকেন্ডে। সাধারণ মানুষের হাতে। বাংলায়।
>
> প্রতিটা ভিডিওর একটা আসল উৎস আছে।
> **আমরা সেটা খুঁজে দিই।**"

**[Final card: OriginX logo + GitHub URL + team name]**

---

## "WOW MOMENTS" — Highlighted for Judge Attention

These are the moments judges will remember. Make sure each one is **clearly visible** on camera:

1. ⚡ **3-second pHash fast-track** (Demo 1) — instant verdict, all agents green
2. 🔴 **Live agent thinking feed** (Demo 2) — 5 agents emitting findings in real-time, terminal-style
3. ⚖️ **"Why this decision?" panel** — color-coded agent badges with weight bars
4. 🌐 **Multilingual RAG chatbot** — Bangla question, Bangla answer with citations
5. 📊 **Counter-card auto-generation** — ready-to-share Bangla PNG

---

## TECHNICAL TALKING POINTS (have ready for Q&A)

**If judge asks "How do you avoid LLM hallucination?":**
> "Adjudicator-এর prompt-এ explicit rules — শুধু provided evidence থেকেই reason করতে পারে, invent করতে পারবে না। Chat-এ RAG context-এই restricted।"

**If judge asks "What's actually AI here vs scripted?":**
> "Real AI: CLIP zero-shot scene classification, EasyOCR multi-script extraction, sentence-transformers multilingual embedding, Groq LLaMA 3.3 70B for synthesis, pgvector cosine similarity, Reciprocal Rank Fusion. Five separate model inferences per frame."

**If judge asks "How does it scale?":**
> "RQ (Redis Queue) handles async investigations. ThreadPoolExecutor runs 4 agents in parallel per video. SSE streaming means hundreds of concurrent users can watch their investigations without polling. PostgreSQL with proper indexing (pgvector for ANN, pg_trgm for fuzzy text)."

**If judge asks "What about deepfakes?":**
> "Roadmap item — ForensicsAgent with HuggingFace deepfake detector. Architecture supports it (parallel agent pool). 14-day plan available."

**If judge asks "Why Bangladesh-specific?":**
> "Bangladesh-এ misinformation pattern unique — পাকিস্তানি/ভারতীয় ভিডিও Bangladesh হিসেবে passed। আমাদের Linguist Urdu/Devanagari script detect করে, Geolocator Pakistani news channel (Geo, ARY) detect করে, our known_cases DB curated Bangladesh incidents দিয়ে। Generic global tool এটা miss করত।"

---

## PRACTICAL FILMING NOTES

- **Screen recording at 1080p minimum.** Use OBS Studio with Display Capture + cursor highlighting.
- **Voice:** Record narration separately, sync in post. Bangla pronunciation should be natural — practice the lines aloud first.
- **Music:** Subtle tense underscore in Segment 1 (problem framing), upbeat tech vibe in demos, calm reflective in closing.
- **Pacing:** Demo segments need exactly the timing shown — if pHash fast-track takes 5 seconds in reality, that's fine, *but cut it in post*. Don't pad.
- **Pre-cache:** Run each demo URL **once before filming** so models are warm (CLIP, embedding model, OCR readers all lazy-loaded). Otherwise first run is 30+ seconds.
- **Browser:** Hide bookmark bar, close other tabs. Use clean browser profile for filming.
- **Demo data:** Make sure DB has at least 3-4 fresh viral videos and a populated TrustGraph for the dashboard segment.

---

## ONE-LINER ELEVATOR PITCH (for if you're cut off at 30 sec)

> "OriginX — ৫টা AI agent মিলে viral ভিডিওর আসল উৎস ৩০ সেকেন্ডে বের করে। Bangladesh misinformation-এর জন্য specifically built। বাংলা-ইংরেজি, real-time streaming, RAG chatbot সহ।"
