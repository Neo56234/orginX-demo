# OriginX — Q&A Prep
# The 10 Hardest Judge Questions + Practiced Answers
# Rule: Every answer must be under 45 seconds. Rehearse until they are.

---

## HOW TO USE THIS FILE

1. Read each question out loud as if a skeptical judge is asking it
2. Answer from memory, not from reading
3. Time yourself — must be under 45 seconds
4. If you go over: cut one point, never the first and last sentence

---

## Q1: "How is this different from InVID?"

**Expected question from:** Any judge with media/tech background

**Your answer:**
> "InVID is the best manual tool available — built by AFP Medialab, used by journalists worldwide. It's excellent. It's also completely manual: a trained journalist clicking through 6 steps for 30 to 90 minutes per video.
>
> OriginX automates that entire workflow, adds visual geo-temporal analysis that InVID doesn't have — we analyze what's inside the frames: text, architecture, license plates — and we output in Bangla, which InVID doesn't.
>
> InVID is built for the 200 journalists in Bangladesh. OriginX is built for the 170 million people who are not journalists.
>
> We're not competing with InVID. We're the citizen layer below it."

**Key points to always hit:** 1) InVID = manual, 2) We add frame-level geo analysis, 3) Bangla output, 4) Different target user.

---

## Q2: "What's your accuracy?"

**Expected question from:** Every technical judge

**Your answer:**
> "On our test set of documented cases from Rumor Scanner and Dismislab — 50 verified Bangladesh misinformation cases — we're achieving [X]% on high-confidence verdicts.
>
> More importantly: when we're not confident, we say so. Below 70% confidence, the system returns 'Insufficient Evidence — recommend manual verification by a professional.' We showed you that case in the demo.
>
> That's a deliberate design choice. A system that's wrong confidently is more dangerous than one that admits uncertainty."

**Key points:** 1) Specific number from your test results, 2) Threshold behavior below 70%, 3) Uncertainty is a feature.

**⚠️ FILL IN THE ACTUAL ACCURACY NUMBER BEFORE DEMO DAY.** Run the pipeline on the 50 seed cases and measure.

---

## Q3: "What if the original video has been deleted?"

**Expected question from:** Technically curious judges

**Your answer:**
> "Three fallback layers. First: Wayback Machine — even deleted content is often archived. We query the CDX API for any snapshot.
>
> Second: our local case database — 50-plus documented cases from Rumor Scanner and Dismislab are pre-loaded. If we've seen this video before, it's an instant verdict regardless of whether the original is gone.
>
> Third: audio fingerprinting. Even if the visual is novel, the audio may match a known case through Chromaprint.
>
> If all three fail, we say Insufficient Evidence. That is the correct answer."

---

## Q4: "How do you handle bias? What if your system falsely flags legitimate content?"

**Expected question from:** Civil society, ethics-focused judges

**Your answer:**
> "Three mechanisms prevent false certainty.
>
> First: confidence thresholds. Below 70% returns Insufficient Evidence, not a verdict. We showed you this case.
>
> Second: every verdict includes full evidence citations. The user sees exactly what signals we detected and where. They can independently verify every claim.
>
> Third: we explicitly say in the interface: 'This is a first-pass screening tool. Confirm with a human fact-checker before publishing.'
>
> We're not replacing human judgment. We're giving citizens the same starting point that journalists have — in under a minute."

---

## Q5: "Could this be used to suppress legitimate protests or political content?"

**Expected question from:** Human rights / press freedom observers

**Your answer:**
> "OriginX analyzes whether a video is being shared with false context. It has no ability to remove or suppress content — it produces evidence, nothing else.
>
> The system can't tell Facebook to take something down. It can't block a share. It generates a report that a human then acts on.
>
> If anything, OriginX protects legitimate protest content — because it distinguishes between 'this is real footage with an accurate caption' versus 'this is real footage with a false caption.' Authentic content gets an Authentic verdict.
>
> Suppression tools operate at the platform level with different mechanisms entirely."

---

## Q6: "What are your data sources for the known cases database?"

**Expected question from:** Research-minded judges

**Your answer:**
> "All public. Rumor Scanner — Bangladesh's largest fact-checking organization — has 3,000 plus verified cases going back to 2020, all publicly accessible. Dismislab has 4,000 plus reports. Fact Watch and BOOM Bangladesh add another 1,300.
>
> We scraped and structured these into our known_cases database — 50 cases for the hackathon, with a clear path to 5,000 post-hackathon.
>
> Every case includes the original false claim, the debunked origin, the actual video date and location, and the source citation. It's fully attributable, fully citable."

---

## Q7: "What about AI-generated deepfakes? Does your system handle those?"

**Expected question from:** Almost everyone

**Your answer:**
> "Different problem, different tools. Sensity, Truepic, and Deepware handle AI-generated manipulation — they look for artifacts inside the video pixel data.
>
> That is not the problem we're solving. The misinformation causing violence in Bangladesh is 100% genuine footage with a false caption. A deepfake detector correctly marks our primary demo video as 'authentic' — and completely misses the lie.
>
> We're the missing piece for the 90% of video misinformation that is real. We're not competing with deepfake detectors — we're complementary to them."

---

## Q8: "How does this scale to thousands of simultaneous requests?"

**Expected question from:** Infrastructure-focused or investor-minded judges

**Your answer:**
> "The architecture is already horizontally scalable. Stateless FastAPI workers behind Redis queue — you add workers, throughput scales linearly. Each investigation is independent with no shared mutable state.
>
> Cost per analysis: approximately three cents in Claude API calls, with everything else on free tiers. At 10,000 analyses per day — our 6-month target — that's $300 per day in cloud costs, fully manageable.
>
> For the hackathon we're on Railway free tier. Production deployment scales to Railway Pro or any container platform. The architecture doesn't change."

---

## Q9: "What's your business model?"

**Expected question from:** Judges evaluating commercial viability

**Your answer:**
> "Three tiers.
>
> Free for citizens forever — that's non-negotiable. A paywall defeats the entire purpose.
>
> API access for newsrooms and fact-checking organizations — $50,000 to $200,000 per year, depending on volume. Eight organizations in Bangladesh alone, plus 40 plus across South Asia.
>
> Enterprise contracts for platforms facing regulatory compliance — Facebook, YouTube, TikTok all face EU Digital Services Act obligations to reduce misinformation. We're an infrastructure component for their compliance stack.
>
> The citizen layer is the mission. The enterprise layer is how we fund it."

---

## Q10: "Why now? Why this team? Why Bangladesh?"

**Expected question from:** Any judge, often the final question

**Your answer:**
> "Why now: Bangladesh saw 142 instances of communal disinformation in just 8 months of 2025, many driven by wrong-context video. The August 2024 uprising showed how lethal this gets — coordinated out-of-context videos, hundreds dead. The urgency is not hypothetical.
>
> Why Bangladesh: 170 million Bangla speakers, second largest Muslim-majority country, eighth most populous nation on earth — and zero automated tools in Bangla for this specific problem. This is a critical gap in a high-stakes environment.
>
> Why this team: We're from here. We understand the visual language, the political context, the platforms people actually use. We built the Bangladesh-specific training into the system from day one, not as an afterthought."

---

## BONUS: Questions you might get that aren't in the top 10

**"Is this open source?"**
> "The core pipeline architecture will be open-sourced post-competition. The Bangladesh-specific model tuning and case database will be open to verified fact-checking organizations under a research license."

**"What if someone uses this to generate false 'Insufficient Evidence' results to muddy the waters?"**
> "The system doesn't take input from external parties on what verdict to return. The evidence pipeline is fully automated and the verdict is generated by the AI from objective signals. You can't social-engineer the Geolocator."

**"How did you build this so fast?"**
> "We used every available open-source component — EasyOCR, CLIP, YOLOv8, Chromaprint — none of these required training from scratch. The innovation is in the orchestration: wiring these tools together into a coherent agent pipeline with a bilingual interface. The engineering challenge was integration, not model training."

---

## WORDS AND PHRASES TO NEVER SAY

| ❌ Never say | ✅ Say instead |
|---|---|
| "We trained custom models" | "We use and fine-tune existing open-source models" |
| "100% accurate" | "[X]% on high-confidence verdicts with uncertainty disclosure below 70%" |
| "Real-time scraping of all platforms" | "We query specific APIs and archives within their terms of service" |
| "It just works" | "Here's specifically how it works..." |
| "I think" (on facts) | Have the number memorized or say "I'll follow up with the exact figure" |
| "We'll add that later" | "That's on our roadmap for Phase [X]" |
| "It's basically like InVID but..." | Don't start comparisons this way — lead with what we do first |
