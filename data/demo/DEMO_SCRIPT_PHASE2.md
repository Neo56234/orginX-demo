# OriginX — "Vibe to Production in 180 Seconds"

**Phase 2 Submission — Infinity AI BuildFest 2026**
**Deadline:** 30 May 2026
**Duration:** 3:00 (strict)

> **Format Rules** (organiser-enforced):
> - 0:00–0:30 → Problem + target users
> - 0:30–1:00 → AI-driven solution
> - 1:00–2:00 → Demo / Concept flow (input → AI → output)
> - 2:00–2:30 → AI Approach (models, RAG, data)
> - 2:30–3:00 → Impact & vision for scaling

প্রতিটা অংশের নিচে শুধু narration একটানা পড়া যাবে। Visual cue আলাদা box-এ।

---

## ০:০০ – ০:৩০ | সমস্যা + Target Users

> **[দৃশ্য:** Facebook timeline দ্রুত scroll। Viral ভিডিওর screenshot — পাকিস্তানি, ভারতীয়, পুরনো বাংলাদেশী ফুটেজ — সবগুলোতে বাংলা caption এবং লাল overlay "ভুয়া"। Share counter ১০ হাজার থেকে লাফিয়ে ৫ লক্ষে পৌঁছাচ্ছে।**]**

আপনি গতকাল একটা মিথ্যা ভিডিও share করেছেন। জানতেন না, আমিও জানতাম না — কারণ যে ভিডিওটা আপনি forward করেছিলেন সেটা ছিল পাকিস্তানের ২০১৯ সালের পুরনো ফুটেজ, আপনি ভেবেছিলেন বাংলাদেশের গতকালের ঘটনা। দশ মিনিটে সেটা পঞ্চাশ হাজার মানুষের কাছে পৌঁছে গেছে, এক ঘণ্টায় পাঁচ লক্ষ।

Bangladesh-এ আমাদের fact-checker রা একটা ভিডিও verify করতে গড়ে সাত ঘণ্টা সময় নেন। ২০২৪-এর আগস্টে এমন এক ভিডিওর কারণে চারজন মানুষ প্রাণ হারিয়েছিলেন — fact-check এসেছিল পরের দিন সকালে, তখন আর কিছু করার ছিল না।

এই সমস্যার ভিকটিম তিন ধরনের মানুষ — সাধারণ Facebook user যিনি গুজব forward করে অপরাধী হয়ে যাচ্ছেন না বুঝেই, journalist আর fact-checker যাঁরা সময়ের যুদ্ধে হারছেন, এবং সরকারি-বেসরকারি platform যাদের misinformation দমন করার tool নেই।

---

## ০:৩০ – ১:০০ | AI-Driven Solution

> **[দৃশ্য:** OriginX লোগো subtle glow-এ ফুটে ওঠে। Tagline: "Every video has a true origin. We find it."**]**

এই সমস্যার সমাধান — OriginX। সাত ঘণ্টার কাজ কুড়ি সেকেন্ডে।

OriginX পাঁচটা specialized AI এজেন্ট-এর একটা team — প্রত্যেকে আলাদা কাজে expert, সবাই একসাথে parallel-এ একটা ভিডিও analyze করে। Tracer খোঁজে এই ভিডিও আগে কোথায় কোথায় ছিল। Chronologist বের করে সর্বপ্রথম কবে online এসেছিল। Geolocator দেখে কোথায় shoot হয়েছে। Linguist পড়ে frame-এর সব text। সবার শেষে Adjudicator — LLaMA 3.3 70B language model — সব evidence ওজন করে চূড়ান্ত verdict দেয়।

User-কে কিছুই করতে হবে না। ভিডিওর link paste করুন বা ফাইল upload করুন, কুড়ি সেকেন্ড অপেক্ষা করুন, বাংলায় verdict পেয়ে যাবেন। AI black-box না — কোন এজেন্ট কী evidence পেয়েছে, প্রতিটার weight কত, পুরো reasoning user-এর সামনে দৃশ্যমান।

---

## ১:০০ – ২:০০ | Demo / System Walkthrough

> **[দৃশ্য:** Browser-এ localhost OriginX হোমপেজ। ক্যামেরা স্ক্রিনের উপর।**]**

আজ দুই ধরনের ভিডিও দিয়ে দেখাবো কীভাবে এটা কাজ করে।

> **[দৃশ্য:** "Me at the zoo" ভিডিও OriginX-এ drag-and-drop। Caption টাইপ: *"এটা গতকাল ঢাকার চিড়িয়াখানার ভিডিও।"* Analyze click। তিন সেকেন্ডের মধ্যেই পাঁচটা agent card সবুজ হয়ে গেলো ✓। Verdict: 99% MISMATCH।**]**

প্রথম ভিডিও — কেউ দাবি করেছেন এটা গতকাল ঢাকার চিড়িয়াখানার ফুটেজ। মাত্র তিন সেকেন্ডে verdict চলে এলো — এটা San Diego Zoo, ২০০৫ সালের ২৩শে এপ্রিল, YouTube-এর ইতিহাসের প্রথম আপলোড করা ভিডিও। এত দ্রুত কীভাবে? OriginX আগে এই ভিডিওর perceptual hash মনে রেখেছিল — Hamming distance algorithm দিয়ে instant match, পুরো investigation skip। একটা ভিডিও একবার ধরা পড়েছে মানে সারাজীবনের জন্য ধরা।

> **[দৃশ্য:** নতুন YouTube URL paste করা — পাকিস্তানি news ভিডিও। Caption: *"বাংলাদেশে আজ হিন্দু সম্প্রদায়ের উপর হামলা।"* Analyze click। পাঁচটা agent card একসাথে "RUNNING" status-এ। Camera নিচের live agent feed-এর উপর zoom in।**]**

দ্বিতীয় ভিডিও — এটা database-এ নেই, আগে কখনো দেখা হয়নি। এবার পাঁচটা agent একসাথে কাজ শুরু করবে। Frame তিনে Geolocator-এর CLIP model বলছে এটা পাকিস্তানি শহুরে রাস্তা ৮৭% confidence-এ। Linguist on-screen text-এ উর্দু script সনাক্ত করেছে — বাংলাদেশের ভিডিওতে উর্দু থাকে না, প্রথম smoking gun। Chronologist Wayback Machine থেকে বের করছে এই ভিডিও ২০২৩-এর আগস্টে archive হয়েছিল। Tracer YouTube-এ একই ভিডিও খুঁজে পেয়েছে — পাকিস্তানের ARY News ২০২৩-এর আগস্টে publish করেছিল, মূল উৎস confirmed।

> **[দৃশ্য:** Adjudicator agent fires — verdict modal slide up। 95% MISMATCH।**]**

Adjudicator চারজনের সব evidence সংগ্রহ করে chain-of-thought reasoning দিয়ে চূড়ান্ত verdict দিল — পাকিস্তানি news ভিডিও, ২০২৩, বাংলাদেশের না। পুরো কাজ কুড়ি সেকেন্ডে। Input ভিডিও → পাঁচটা AI parallel-এ analysis → স্বচ্ছ reasoning সহ output। সাত ঘণ্টা বনাম কুড়ি সেকেন্ড — এক হাজার গুণের চেয়েও দ্রুত।

---

## ২:০০ – ২:৩০ | AI Approach — Models, RAG, Data

> **[দৃশ্য:** Architecture diagram — পাঁচটা agent কেন্দ্রের Adjudicator-এ converge করছে। ডানে separate panel-এ tech stack চিহ্ন: CLIP, EasyOCR, pgvector, LLaMA, Redis।**]**

Technical স্তরে কী চলছে দেখাই।

Geolocator OpenAI-এর CLIP ViT-B/32 model দিয়ে zero-shot scene classification করে — প্রতিটা frame-এ বারোটা region-এর মধ্যে কোনটা match হচ্ছে softmax confidence দিয়ে নির্ধারিত। Linguist EasyOCR দিয়ে multi-script text extraction চালায় — বাংলা, হিন্দি, উর্দু, আরবি, ইংরেজি — দুটো parallel reader thread-lock-এ চলে। Tracer perceptual hash (pHash) compute করে Hamming distance threshold-এ near-duplicate detect করে এবং Yandex reverse image search + YouTube Data API call করে।

Adjudicator-এ Groq cloud-এ LLaMA 3.3 70B model — JSON-structured output, temperature 0.1, explicit anti-hallucination rules যাতে শুধু provided evidence থেকেই reason করে।

আমাদের chatbot Knowledge Base-এ Hybrid RAG — PostgreSQL-এর tsvector BM25 full-text search, pgvector cosine similarity-তে semantic search (paraphrase-multilingual-MiniLM-L12-v2 embedding দিয়ে), এবং Reciprocal Rank Fusion দিয়ে দুটো result merge। সব data PostgreSQL-এ — pgvector ANN indexing, pg_trgm fuzzy text। Async pipeline চলে Redis Queue-এ, পাঁচটা agent ThreadPoolExecutor parallel-এ, real-time streaming Server-Sent Events দিয়ে।

---

## ২:৩০ – ৩:০০ | Impact & Vision for Scaling

> **[দৃশ্য:** Black screen-এ slow fade।**]**

আজ থেকে ছয় মাস পর — বাংলাদেশের একজন মা, যাঁর ছেলে হয়তো গুজবের ভিকটিম হতে পারতেন — তিনি একটা ভিডিও পান, share করার আগে OriginX-এ check করেন, ভুয়া পান, forward করেন না। একটা পরিবার বাঁচে। এটা hackathon project না — এটা একটা public weapon, গুজবের বিরুদ্ধে।

> **[দৃশ্য:** Scaling roadmap diagram — চারটা phase visible।**]**

Scale করার vision চারটা phase-এ। প্রথম phase-এ — সাধারণ user-এর জন্য WhatsApp bot, যেকোনো বাংলাদেশী মা-বাবা ভিডিও forward করে instant verdict পাবেন। দ্বিতীয় phase-এ — Facebook এবং Newspaper এডিটোরিয়াল-এর সাথে API integration, যাতে publishing-এর আগে automatic verification হয়। তৃতীয় phase-এ — Forensics Agent যোগ করে deepfake detection, এবং multilingual coverage বাড়িয়ে Hindi, Urdu, English content। চতুর্থ phase-এ — সরকারি Election Commission আর Press Council-এর জন্য monitoring dashboard, যাতে coordinated misinformation campaign রিয়েল টাইমে detect হয়।

> **[দৃশ্য:** OriginX লোগো centered, tagline নিচে।**]**

প্রতিটা ভিডিওর একটা আসল উৎস আছে। আমরা সেটা খুঁজে দিই।

---

## 🎤 Voice-over Tips

- প্রতিটা অংশের আগে কয়েক সেকেন্ড breathing space নিন।
- ০:০০-০:৩০ — Slow, accusatory tone। "আপনি গতকাল একটা মিথ্যা ভিডিও share করেছেন" — সরাসরি challenge।
- ০:৩০-১:০০ — Confident, deliberate। Solution বলার সময় calm authority।
- ১:০০-২:০০ — Energetic, sports-commentary style demo-এর agent finding বলার সময়।
- ২:০০-২:৩০ — Technical, precise। Models আর architecture বলার সময় expert tone।
- ২:৩০-৩:০০ — Slow, emotional। "একটা পরিবার বাঁচে" বলার পর ১.৫-২ সেকেন্ড চুপ।

## 🎵 Music Cues

| সময় | Mood |
|------|------|
| 0:00 – 0:30 | Low drone, tension building |
| 0:30 – 1:00 | Hopeful synth pulse, solution arriving |
| 1:00 – 2:00 | Tech-thriller active score |
| 2:00 – 2:30 | Steady, intelligent — "behind the scenes" feel |
| 2:30 – 3:00 | Soft piano only, emotional landing |

## 🚨 শুটিং-এর আগে চেকলিস্ট

- দুটো demo URL আগে warm-up রান করুন (CLIP, OCR, embedding model lazy-load করে — first run ৩০ সেকেন্ড)।
- "Me at the zoo" video file ready রাখুন drag-drop-এর জন্য।
- দ্বিতীয় demo-র জন্য একটা পরিচিত পাকিস্তানি/ভারতীয় news ভিডিওর YouTube URL ready রাখুন (যেটা download হবে নিশ্চিতভাবে)।
- Browser bookmark bar hide, অন্য সব tab close, Phone DND-তে।
- Voice-over আলাদা record করে post-এ sync করুন। Screen recording mute রাখুন।
- Stopwatch ধরে script ৩ বার পড়ুন — প্রতিটা segment নির্ধারিত সময়ের মধ্যে শেষ হতে হবে।
- Demo-র real time যদি ২৫ সেকেন্ড হয় কিন্তু segment-এর জন্য আছে ২০ সেকেন্ড, post-এ aggressive cut করুন।

## ⏱️ Timing Sanity Check

Voice-over পড়ার সময় প্রতিটা segment-এর সর্বোচ্চ word count:

| Segment | Time | আনুমানিক বাংলা শব্দ |
|---------|------|---------------------|
| Problem | 30s | ~70-80 শব্দ |
| Solution | 30s | ~70-80 শব্দ |
| Demo | 60s | ~140-160 শব্দ |
| AI Approach | 30s | ~70-80 শব্দ |
| Impact | 30s | ~70-80 শব্দ |

আমাদের script এই word count-এর মধ্যে আছে — কিন্তু practice করে confirm করুন।

## 🔥 Backup Pitch (যদি ৩০ সেকেন্ডে কেউ জিজ্ঞেস করেন)

Bangladesh-এ একটা viral ভিডিও verify করতে fact-checker রা গড়ে সাত ঘণ্টা নেন — ততক্ষণে পাঁচ লক্ষ মানুষ সেটা share করে ফেলে। OriginX সেই কাজটা পাঁচটা AI agent দিয়ে কুড়ি সেকেন্ডে করে। বাংলায়, real-time live agent streaming সহ, RAG-powered chatbot সহ, instant counter-card সহ, WhatsApp bot সহ। Phase 1-এ সাধারণ user, Phase 4-এ সরকারি Election Commission monitoring। Hackathon project না — public weapon।
