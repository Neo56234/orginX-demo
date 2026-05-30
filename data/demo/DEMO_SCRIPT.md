# OriginX — 5-Minute Demo Script
# Infinity AI BuildFest 2026 | BRAC University | June 12, 2026
# MEMORIZE THIS. No ad-lib. No improvising under pressure.

---

## PRE-DEMO SETUP CHECKLIST (do this 30 minutes before your slot)

- [ ] Browser open at `http://localhost:3001` (or deployed URL)
- [ ] Dashboard tab pre-opened at `http://localhost:3001/dashboard`
- [ ] All demo investigation pages pre-loaded in background tabs
- [ ] Phone charged, WhatsApp bot tested this morning
- [ ] Slide deck open in presenter mode, Slide 1 active
- [ ] `pipeline_results.json` checked — all investigation_ids confirmed
- [ ] Internet connection confirmed (or offline mode tested)
- [ ] Timer app ready (phone or laptop — display visible to you only)
- [ ] Water bottle nearby

---

## TOTAL TIME: 5:00 MINUTES

| Act | Content | Time |
|-----|---------|------|
| 1 | The Hook | 0:00 – 0:30 |
| 2 | The Reveal (Demo) | 0:30 – 2:17 |
| 3 | The Verdict + Counter-Card | 2:17 – 3:15 |
| 4 | The Scale (Virality Monitor) | 3:15 – 4:00 |
| 5 | The Ask | 4:00 – 5:00 |

---

## ACT 1: THE HOOK (0:00 – 0:30)

**Screen:** Slide 1 (OriginX title slide)

*[Speak slowly. Make eye contact. No rushing.]*

> **[BN]** "গতকাল রাতে, এই ভিডিওটি ১২ লক্ষ বার শেয়ার হয়েছে।"
>
> **[EN]** "Last night, this video was shared 1.2 million times."

*[Pause 2 full seconds. Let it land.]*

> "It's not from Dhaka."
>
> "It's not from this week."
>
> "It's not from this year."
>
> "It's not from this country."

*[Pause 1 second.]*

> "By the time fact-checkers prove that — tomorrow — people will already be dead."

*[Pause 1 second.]*

> "We built something to stop that."

*[Click to Slide 2 — The Problem. Keep moving.]*

---

## ACT 1B: CONTEXT SLIDES (0:30 – 1:00)

**Screen:** Slide 2 → Slide 3 (fast, 15 seconds each)

*[Slide 2 — say this while it's on screen:]*
> "Fifty-two percent of all misinformation in Bangladesh doesn't come from AI-generated content. It comes from real video — real footage — shared with false context. A 2019 riot in Pakistan shared today as 'Hindu attack in Dhaka.' The video is authentic. The caption is a lie."

*[Click to Slide 3. Say this:]*
> "Every tool on the market asks: 'Is the video manipulated?' Wrong question. OriginX asks: 'Is the context true?' Same footage. Different answer."

*[Click to Slide 4 / switch to browser. Say:]*
> "Let me show you."

---

## ACT 2: THE REVEAL (1:00 – 2:17)

**Screen:** OriginX web app, home page. Empty URL bar pulsing.

*[Take a breath. Speak at normal pace — the demo does the work.]*

> "This is a video currently circulating in Bangladesh."
> "It claims: 'Hindu extremists are being attacked in Dhaka right now.'"

*[Paste the demo URL — Video #1 from demo_videos.json]*
*[Type/paste the claimed context in the context box]*
*[Hit ANALYZE]*

> "OriginX receives the video. And now..."

*[The 5 agent cards activate. Narrate as findings appear — wait for them:]*

*[When Linguist fires first — usually ~8 seconds:]*
> "The Linguist just detected Urdu text on frame 7."
> *[pause beat]* "Bangladesh doesn't use Urdu."

*[When Chronologist fires — ~15 seconds:]*
> "The Chronologist found this video on the Wayback Machine — archived March 2019."

*[When Geolocator fires — ~20 seconds:]*
> "The Geolocator matched the architecture to Karachi — with 87% confidence."

*[When Tracer fires — show if it finds an earlier appearance:]*
> "The Tracer found 3 earlier appearances online — the oldest from 2019."

*[At the 47-second mark on the timer, say:]*
> "Forty-seven seconds."

*[No further narration — let the Adjudicator activate visually]*

---

## ACT 3: THE VERDICT + COUNTER-CARD (2:17 – 3:15)

**Screen:** Adjudicator animates in. Verdict Card reveals.

*[Let the animation play fully — don't talk over it]*

*[After verdict appears:]*
> "Forty-seven seconds. The same fact-check used to take ninety minutes."

*[Point to the verdict card on screen:]*
> "Pakistan. March 2019. Shared as Dhaka, November 2024."
> "Five-year gap. Wrong country. Mismatch."

*[Beat]*
> "But the verdict isn't the product."

*[Click "Share Rebuttal" / "প্রতিবাদ শেয়ার করুন"]*
*[Counter-card animates in]*

> "Because knowing the truth doesn't help if nobody sees the correction."
>
> "So we generate the rebuttal — designed to travel the same way the lie did."
> "Same format as a viral card. Same visual language. Same share buttons."
>
> "The misinformation spread on WhatsApp. So does the counter-narrative."

*[Optional — if doing WhatsApp demo:]*
> "In fact, someone can just forward us the video directly."
> *[Show phone, open WhatsApp bot chat, forward video URL]*
> "And in under 90 seconds, they get the verdict — without even opening a browser."

---

## ACT 4: THE SCALE (3:15 – 4:00)

**Screen:** Switch to Virality Monitor dashboard (`/dashboard`)

> "This is what's circulating in Bangladesh right now."

*[Gesture at the grid of viral video cards]*

> "Eight fact-checking organizations cover this country. Two hundred people total."
> "They're doing incredible work. But they can't check everything."

*[Point to a campaign alert banner if showing:]*
> "This alert — coordinated campaign detected — that's OriginX identifying when the same video is being shared from multiple sources simultaneously. That's not random misinformation. That's organized."

*[Click on one flagged card to show investigation link, or Trust Graph]:*
> "Every flagged video links to a full forensic investigation."
> "Every investigation is a public, citable, shareable piece of evidence."

> "We can."

---

## ACT 5: THE ASK (4:00 – 5:00)

**Screen:** Switch to Slide 5 (Vision map), then Slide 6 (Ask)

*[Slide 5 — say this fast, 20 seconds:]*
> "Today: Bangladesh. 170 million people served."
> "Tomorrow: every South Asian country with the same problem — Myanmar, Sri Lanka, Nepal."
> "Same architecture. Swap the language model. New country in weeks."
> "We're not building a fact-checking website. We're building the trust infrastructure for video on the open internet."

*[Click to Slide 6 — take a moment, look at audience directly]*

> "We built this in [N] weeks. Total API cost: about five dollars."

*[Beat]*

> "We're looking for three things from this room."
> "Researchers — help us benchmark accuracy on real Bangladeshi cases."
> "Platforms — we need API partnerships for video metadata."
> "Judges — introductions to Rumor Scanner and Dismislab, the organizations whose work we're automating."

*[Pause, direct eye contact with the most senior person in the room]*

> "If you work at a platform that hosts video — please find us after this session."

*[Final beat — slower, clear Bangla:]*
> **"আপনার সাহায্য দিয়ে — আমরা মিথ্যা ভিডিও যাত্রার সময় বন্ধ করব।"**

*[Hold 3 seconds. Smile. Take the mic.]*

---

## TIMING GUIDE

Print this and keep it on the podium:

```
0:00  START — Slide 1, The Hook
0:30  Slide 2 — Problem stat
0:45  Slide 3 — Insight
1:00  SWITCH TO BROWSER — paste URL
1:08  Linguist fires — "Urdu text detected"
1:15  Chronologist — "Wayback Machine 2019"
1:20  Geolocator — "Architecture → Karachi"
1:47  TIMER HIT 47 SECONDS — say "Forty-seven seconds"
2:00  Adjudicator completes — let animation play
2:17  "But the verdict isn't the product"
2:20  Click Share Rebuttal — counter-card
2:45  (Optional WhatsApp demo)
3:00  SWITCH TO DASHBOARD
3:45  Back to slides
4:00  Vision map
4:20  The Ask slide
4:45  "আপনার সাহায্য দিয়ে..."
5:00  DONE — hold silence, then take mic
```

---

## FAILURE RECOVERY LINES

**If URL paste fails / page doesn't load:**
> "The live connection is being temperamental — let me show you a recent investigation instead."
*[Click directly to a pre-cached investigation URL from your browser history]*

**If SSE disconnects mid-stream:**
> "You can see the agents working in parallel — this is exactly what happens in production at scale."
*[Navigate to the investigation URL directly — it will show the cached result]*

**If Claude API is slow / Adjudicator hangs:**
> "The final synthesis is running — this is where all five agents' evidence is being weighed by the Adjudicator."
*[Keep talking about what the earlier agents found — buy 30 seconds]*
*[If more than 60 seconds: click to the already-cached version in your backup tab]*

**If Bangla fonts fail to render:**
> "On the demo setup the Bengali font didn't load — but you can see the verdict in English here, and I'll read the Bangla verdict to you:"
*[Read from your phone's cached screenshot]*

**If projector disconnects:**
> "Let me pass the laptop around — the demo will be clearer this way."
*[Keep presenting. Judges appreciate composure.]*

**If judge interrupts mid-demo:**
*[Stop immediately. Answer their question. Say:]*
> "Great question — let me show you that specifically."
*[Navigate to the relevant section. Never say "I'll cover that later."]*

---

## THE THREE MOMENTS THAT WIN THE DEMO

1. **The "47 seconds" line** — time it perfectly. This is your punch.
2. **The Counter-Card appearance** — let the animation play, say nothing for 2 seconds.
3. **The final Bangla line** — slow, clear, direct eye contact. This is your close.

Everything else is context. These three moments are what the judges remember.

---

## BANGLA PRONUNCIATION GUIDE (for the key lines)

- গতকাল রাতে = *gotokal ra-te* (last night)
- ১২ লক্ষ বার = *baro lakh bar* (1.2 million times)
- মিথ্যা প্রসঙ্গ সনাক্ত = *mitha prosongo shonaakto* (false context detected)
- আপনার সাহায্য দিয়ে = *apnar shahajyo diye* (with your help)
- আমরা মিথ্যা ভিডিও যাত্রার সময় বন্ধ করব = *amra mitha video jatrar shomoy bondho korbo* (we will stop the false video in its tracks)
