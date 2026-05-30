# OriginX — ৩ মিনিটের ডেমো স্ক্রিপ্ট

**Tip:** এটা পড়ার জন্য লেখা — দেখানোর জন্য না। প্রতিটা অনুচ্ছেদ একটানা পড়া যায়। Visual cue আলাদা box-এ। শুধু narration-এর অংশই পড়লেই হবে।

---

## অংশ ১ — শুরুর ধাক্কা (0:00 – 0:25)

> **[দৃশ্য:** কালো স্ক্রিন। কয়েক সেকেন্ড Facebook timeline scroll — viral ভিডিওর screenshot ভেসে আসছে।**]**

আপনি গতকাল একটা মিথ্যা ভিডিও share করেছেন। জানতেন না, আমিও জানতাম না — কারণ যে ভিডিওটা আপনি forward করেছিলেন সেটা ছিল পাকিস্তানের ২০১৯ সালের পুরনো ফুটেজ, আপনি ভেবেছিলেন বাংলাদেশের গতকালের ঘটনা। দশ মিনিটে সেটা পঞ্চাশ হাজার মানুষের কাছে পৌঁছে গেছে, এক ঘণ্টায় পাঁচ লক্ষ। Fact-checker রা verify করতে শুরু করেছেন — সময় লাগবে গড়ে সাত ঘণ্টা।

> **[দৃশ্য:** স্ক্রিনে বড় লাল কাউন্টার — "7 hours" — পাশে ছোট হরফে "average fact-check time"।**]**

এই সাত ঘণ্টায় কী হয় জানেন? ২০২৪-এর আগস্টে এমন এক ভিডিওর কারণে চারজন মানুষ প্রাণ হারিয়েছিলেন। Fact-check এসেছিল পরের দিন সকালে — তখন আর কিছু করার ছিল না।

আমরা সেই সাত ঘণ্টাকে কুড়ি সেকেন্ডে নামিয়ে এনেছি।

> **[দৃশ্য:** OriginX লোগো subtle glow-এ ফুটে ওঠে।**]**

---

## অংশ ২ — সমাধান-এর পরিচয় (0:25 – 0:40)

> **[দৃশ্য:** Presenter সরাসরি camera-র দিকে তাকিয়ে।**]**

আজ এই room-এ যাঁরা বসে আছেন তাঁদের সবার পকেটে একটা phone আছে, এবং পরের এক ঘণ্টায় সেই phone-এ অন্তত তিনটা ভিডিও আসবে যেগুলো ভুয়া। আপনি বুঝতে পারবেন না, কেউই বুঝতে পারে না — অন্তত এতদিন পারত না।

আমার পেছনে এই স্ক্রিনে যা চলছে সেটার নাম OriginX। পাঁচটা AI এজেন্ট একসাথে parallel-এ কাজ করে যেকোনো viral ভিডিওর আসল উৎস বের করে আনে। আপনাকে কিছুই করতে হবে না — শুধু paste করুন, আর অপেক্ষা করুন কুড়ি সেকেন্ড।

আজ তিন ধরনের ভিডিও দিয়ে এটা প্রমাণ করব।

---

## অংশ ৩ — প্রথম ডেমো: pHash Fast-Track (0:40 – 1:00)

> **[দৃশ্য:** "Me at the zoo" ভিডিও OriginX-এ drag-and-drop। Caption টাইপ করা — *"এটা গতকাল ঢাকার চিড়িয়াখানার ভিডিও।"* Analyze button click।**]**

প্রথম ভিডিও — কেউ দাবি করেছেন এটা গতকাল ঢাকার মিরপুর চিড়িয়াখানার ফুটেজ। দেখি কী বের হয়।

> **[দৃশ্য:** তিন সেকেন্ডের মধ্যেই পাঁচটা agent card-ই সবুজ হয়ে গেলো ✓। Verdict modal slide up — 99% MISMATCH।**]**

মাত্র তিন সেকেন্ড। এটা মিরপুর চিড়িয়াখানার ভিডিও না — এটা San Diego Zoo, ২০০৫ সালের ২৩শে এপ্রিল, YouTube-এর ইতিহাসের প্রথম আপলোড করা ভিডিও।

এত দ্রুত কীভাবে হলো? OriginX আগে এই ভিডিওটার pHash — মানে perceptual fingerprint — মনে রেখেছিল। নতুন কেউ এই ভিডিও দিয়ে গুজব ছড়াতে চাইলে — Hamming distance algorithm দিয়ে instant match, পুরো investigation skip। অর্থাৎ একটা ভিডিও যেটা একবার ধরা পড়েছে, সেটা সারাজীবনের জন্য ধরা।

---

## অংশ ৪ — দ্বিতীয় ডেমো: Full Pipeline (1:00 – 1:30)

> **[দৃশ্য:** নতুন একটা YouTube URL paste করা — পাকিস্তানি একটা news ভিডিও। Caption: *"বাংলাদেশে আজ হিন্দু সম্প্রদায়ের উপর হামলা।"* Analyze click। পাঁচটা agent card একসাথে "RUNNING" হয়।**]**

এবার একটা ভিডিও যেটা database-এ নেই, আগে কখনো দেখা হয়নি। দেখুন AI কীভাবে শিকার করে।

> **[দৃশ্য:** Camera নিচের live feed-এর উপর zoom in।**]**

Frame তিনে Geolocator কথা বলছে — ক্যামেরায় যা দেখছে সেটা পাকিস্তানি শহুরে রাস্তা, ৮৭% confidence। Frame দুইয়ে Linguist on-screen text-এ উর্দু script সনাক্ত করেছে — বাংলাদেশের ভিডিওতে উর্দু থাকে না, এটাই প্রথম smoking gun। এদিকে Chronologist Wayback Machine থেকে বের করছে যে এই ভিডিও archive হয়েছিল ২০২৩-এর আগস্টে — অর্থাৎ এটা আজকের ভিডিও না, দ্বিতীয় smoking gun। Tracer YouTube-এ একই ভিডিও খুঁজে পেয়েছে — পাকিস্তানের ARY News ২০২৩-এর আগস্টে publish করেছিল, মূল উৎস confirmed।

এবার Adjudicator — চারজনের সব evidence নিয়ে Groq-এ LLaMA 3.3 70B model call করে chain-of-thought reasoning দিয়ে চূড়ান্ত verdict বের করে।

> **[দৃশ্য:** Verdict modal: 95% MISMATCH।**]**

পুরো কাজ কুড়ি সেকেন্ডে। সাত ঘণ্টা বনাম কুড়ি সেকেন্ড — এক হাজার গুণের চেয়েও দ্রুত। এবং খেয়াল করুন — AI black-box না। কোন এজেন্ট কী evidence দিয়েছে, প্রতিটার weight কত, পুরোটাই user দেখতে পাচ্ছে।

---

## অংশ ৫ — তৃতীয় ডেমো: Honest AI (1:30 – 1:45)

> **[দৃশ্য:** এমন একটা YouTube link paste করা যেটা download-এ block। Tracer feed-এ message: "Video download blocked — running URL-only analysis."**]**

আপনারা ভাবছেন — সব ভিডিও তো download করা যায় না, তাহলে? দেখি।

YouTube এই link block করে রেখেছে — ভিডিও download হলো না। কিন্তু OriginX থেমে যাবার সিস্টেম না — Channel metadata, archive data, YouTube API থেকে যা পাওয়া যায় সব দিয়ে best-effort analysis চালিয়ে যায়।

> **[দৃশ্য:** Verdict — "Insufficient Evidence" with proper reasoning।**]**

এবং সবচেয়ে important — confidence কম হলে OriginX মিথ্যা answer বানিয়ে দেয় না, সরাসরি বলে দেয় "যথেষ্ট প্রমাণ নেই।" এটাই production-grade AI — honest, যা জানে না সেটা বলে দেয়।

---

## অংশ ৬ — এজেন্টদের পরিচয় (1:45 – 2:15)

> **[দৃশ্য:** Architecture diagram — পাঁচটা agent card hexagon-এ সাজানো, কেন্দ্রে Adjudicator।**]**

এই পাঁচটা agent কারা? এটা যেন একটা সিনেমার team, প্রত্যেকের আলাদা role।

**Tracer — The Detective।** ভিডিওটা আগে কোথায় কোথায় ছিল সেটা খোঁজে। Yandex reverse image search, YouTube API, আমাদের নিজস্ব pHash database — তিন জায়গায় scan করে duplicate খুঁজে বের করে।

**Chronologist — The Time-Traveler।** এই ভিডিও সর্বপ্রথম কবে online এসেছিল? Wayback Machine-এর CDX API আর YouTube publication date দিয়ে earliest evidence বের করে আনে।

**Geolocator — The Cartographer।** কোথায় shoot হয়েছে? OpenAI-এর CLIP model দিয়ে zero-shot scene classification, সাথে Pakistani আর Indian news channel — Geo News, ARY, India Today, NDTV — সবার নাম on-screen text-এ থাকলে চিনে ফেলে।

**Linguist — The Polyglot।** Frame-এ যত লেখা আছে সব পড়ে। EasyOCR দিয়ে বাংলা, হিন্দি, উর্দু, আরবি, ইংরেজি — multi-script extraction। উর্দু পেলে সেটা বাংলাদেশের ভিডিও না, confirmed।

**Adjudicator — The Judge।** চারজনের সব evidence সংগ্রহ করে। Groq-এ LLaMA 3.3 70B model — chain-of-thought reasoning দিয়ে চূড়ান্ত verdict। এবং সবচেয়ে important, কেন এই সিদ্ধান্ত নিলো, প্রতিটা evidence-এর weight সহ user-কে দেখায়। AI যেটা নিজের কাজ explain করে।

---

## অংশ ৭ — বাকি Features (2:15 – 2:40)

> **[দৃশ্য:** চারটা feature দ্রুত montage, প্রতিটা ৫-৬ সেকেন্ড করে।**]**

এটা শুধু একটা analyzer না, এটা একটা ecosystem।

**প্রথমে Knowledge Base।** Chat page-এ বাংলায় প্রশ্ন করুন — "শাপলা চত্বরের পুরনো ভিডিও কী কী এখন viral হচ্ছে?" — বাংলায় উত্তর আসবে, citation সহ। Behind the scene কী চলছে? Hybrid RAG — BM25 full-text search PostgreSQL-এ, semantic vector search pgvector-এ, এবং Reciprocal Rank Fusion দিয়ে দুটো merge। LLM hallucinate করতে পারবে না, শুধু আমাদের verified database থেকেই উত্তর দেবে।

**দ্বিতীয়ত Viral Monitor Dashboard।** কে বারবার ভুয়া ছড়াচ্ছে, কোন ভিডিও coordinated network থেকে spread হচ্ছে — সব track। Campaign Detector — একই pHash যদি ৪৮ ঘণ্টার মধ্যে তিনবার বা তার বেশি ধরা পড়ে, automatically campaign হিসেবে flag।

**তৃতীয়ত Counter-Card Generator।** Mismatch detect হলে instant একটা বাংলা PNG তৈরি হয় — Facebook, WhatsApp, যেখানে খুশি এক click-এ share। গুজবের জবাব দিতে আর হাঁপাতে হবে না।

**চতুর্থত WhatsApp Bot।** যাঁরা website use করতে comfortable না, আপনার মা-বাবার-ও জন্য — ভিডিও link forward করুন, ত্রিশ সেকেন্ডে বাংলায় verdict ফিরে আসবে।

---

## অংশ ৮ — শেষ কথা (2:40 – 3:00)

> **[দৃশ্য:** Black screen-এ slow fade।**]**

আজ থেকে ছয় মাস পর — বাংলাদেশের একজন মা, যাঁর ছেলে হয়তো গুজবের ভিকটিম হতে পারতেন — তিনি একটা ভিডিও পান, share করার আগে OriginX-এ check করেন, ভুয়া পান, forward করেন না। একটা পরিবার বাঁচে।

এটা hackathon project না — এটা একটা public weapon, গুজবের বিরুদ্ধে।

> **[দৃশ্য:** OriginX লোগো center-এ। নিচে slowly fade in tagline।**]**

প্রতিটা ভিডিওর একটা আসল উৎস আছে। আমরা সেটা খুঁজে দিই।

---

## 🎤 Voice-over Tips

- প্রতিটা অনুচ্ছেদ একবার শুরু করলে শেষ না করে থামবেন না।
- লাল কাউন্টার বা verdict modal আসার মুহূর্তে narration একটু থামিয়ে দর্শককে স্ক্রিন দেখতে দিন (এক-দুই সেকেন্ড)।
- ডেমো ২-এর agent finding-গুলোর narration sports commentary tone-এ — energy, কিন্তু শব্দ একটানা।
- শেষ অনুচ্ছেদ ("আজ থেকে ছয় মাস পর...") — speed ধীর, কণ্ঠ নিচু। "একটা পরিবার বাঁচে।" বলার পর ২-৩ সেকেন্ড একদম চুপ।

## 🎵 Music Cues

| সময় | Mood |
|------|------|
| 0:00 – 0:25 | Low drone। প্রায় silent। Tension। |
| 0:25 – 0:40 | Synth pulse build। |
| 0:40 – 1:45 | Tech-thriller active score। |
| 1:45 – 2:40 | Rising, hopeful। |
| 2:40 – 3:00 | শুধু soft piano। Drop everything else। |

## 🚨 শুটিং-এর আগে চেকলিস্ট

- প্রতিটা demo URL একবার warm-up রান করুন (model lazy-load করে — first run ৩০ সেকেন্ড)।
- Browser-এ অন্য সব tab close, bookmark bar hide।
- Phone Do Not Disturb-এ রাখুন।
- Voice-over আলাদা record করে post-এ sync করুন। Screen recording mute।
- Stopwatch ধরে script ৩ বার পড়ুন — ৩:০০-এর মধ্যে শেষ না হলে দীর্ঘ অনুচ্ছেদ trim করুন।

## 🔥 Backup Pitch (যদি ৩০ সেকেন্ডে কেউ জিজ্ঞেস করেন)

বাংলাদেশে একটা viral ভিডিও verify করতে fact-checker রা গড়ে সাত ঘণ্টা নেন — ততক্ষণে পাঁচ লক্ষ মানুষ সেটা share করে ফেলে। OriginX সেই কাজটা পাঁচটা AI agent দিয়ে কুড়ি সেকেন্ডে করে দেয়। বাংলায়, real-time live agent streaming সহ, RAG-powered chatbot সহ, instant counter-card সহ, WhatsApp bot সহ। Hackathon project না — public weapon।
