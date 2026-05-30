# OriginX — Demo Day Checklist
# Run this 24 hours before the competition and again 1 hour before your slot.

---

## T-24 HOURS (June 11, 2026 — the day before)

### Code Freeze ✋
- [ ] No new code after this point — no "quick fixes", no "small improvements"
- [ ] `git status` is clean — no uncommitted changes
- [ ] Both Railway (backend) and Vercel (frontend) builds are GREEN
- [ ] GitHub Actions CI is passing

### Pipeline Cache Verification
- [ ] `run_pipeline.ps1` completed successfully (all videos in `pipeline_results.json`)
- [ ] All 3 primary demo videos have `investigation_id` values
- [ ] All 3 primary investigation pages load correctly in browser
- [ ] All 3 counter-cards accessible via `/share/{id}` URLs
- [ ] `verify_cards.ps1` shows all cards as EXISTING (not MISSING)
- [ ] At least 7 out of 10 demo videos produce correct expected verdict

### Offline Backup
- [ ] USB drive prepared with:
  - [ ] `backup_demo.mp4` — recorded screen capture of full 5-minute demo run
  - [ ] `pipeline_results.json` — all investigation IDs and results
  - [ ] `PITCH_DECK.pdf` — PDF export of slide deck
  - [ ] `DEMO_SCRIPT.md` — printed copy (physical backup)
  - [ ] Screenshots of each investigation result page (in case browser fails)
- [ ] Offline JSON cache: for each primary demo video, save the full investigation JSON response to `/data/demo/offline/{investigation_id}.json`

### Communication Channels
- [ ] WhatsApp bot tested with your personal phone TODAY
  - Forward primary demo video URL → receive verdict reply within 90 seconds
- [ ] Test on phone data (NOT home WiFi) — simulate venue conditions
- [ ] Twilio sandbox still active (check console.twilio.com)

### Visual Quality
- [ ] Bangla fonts render correctly at 1920×1080 on the demo machine
- [ ] VerdictCard Bangla text is readable at 3 meters distance
- [ ] All agent emoji icons visible on projector (test at projector resolution)
- [ ] Dashboard viral monitor loads with seed data populated

### Slide Deck
- [ ] Final version exported as PDF
- [ ] PDF on USB drive
- [ ] QR code tested — links to correct URL
- [ ] Team contact info on slide 6 is current
- [ ] Fill in actual accuracy number in QA_PREP.md Q2 (run pipeline on 50 seed cases)

---

## T-1 HOUR (June 12, 2026 — demo day, your slot minus 60 minutes)

### Environment Check
- [ ] Open browser to `http://localhost:3001` (or deployed URL) — confirm it loads
- [ ] Open dashboard tab — confirm viral monitor has data
- [ ] Open all 3 primary investigation pages in background tabs
  - Tab 1: `http://localhost:3001/investigation/{id_1}` (Video #1 — primary demo)
  - Tab 2: `http://localhost:3001/investigation/{id_3}` (Video #3 — backup)
  - Tab 3: `http://localhost:3001/dashboard`
  - Tab 4: Slide deck (Google Slides / PDF)
- [ ] Confirm SSE stream replays correctly on the primary investigation page
- [ ] Confirm Mapbox map tiles are loaded (both pins visible)
- [ ] Confirm counter-card is visible on `/share/{id_1}`

### Network
- [ ] Connected to venue WiFi — confirm it works
- [ ] If venue WiFi is slow/unreliable: switch to phone hotspot (test now)
- [ ] SSE stream test: open investigation page → confirm agent cards animate
- [ ] If SSE is blocked: fallback polling works (check `lib/sse.ts` polling mode)

### Hardware
- [ ] Laptop charged to 100% (bring charger regardless)
- [ ] Phone charged to 100%
- [ ] Presentation clicker works (if using one)
- [ ] HDMI adapter in bag (if demo machine differs from yours)
- [ ] Second HDMI adapter as backup

### Personal
- [ ] Water bottle filled
- [ ] Timer app ready on phone (don't use the same phone as WhatsApp demo)
- [ ] DEMO_SCRIPT.md reviewed — ran through the 47-second moment
- [ ] QA_PREP.md reviewed — all 10 answers fresh in memory
- [ ] Team knows who speaks which sections

---

## T-30 MINUTES (Slot minus 30 minutes)

### Final Run-Through
- [ ] Full 5-minute demo rehearsed once (no interruptions)
- [ ] Timer verified: 47-second mark on the demo video
- [ ] Each team member knows their recovery line for each failure mode
- [ ] Browser zoom level set correctly (not too zoomed in or out for projector)
- [ ] Dark mode on OS (so taskbar/notifications don't show light elements)
- [ ] Notifications muted (Do Not Disturb mode ON)
- [ ] Close all non-demo browser tabs (except the 4 demo tabs)

---

## T-5 MINUTES (On deck, about to present)

1. Deep breath
2. Slide 1 is showing on screen
3. Water bottle placed at podium
4. Phone with WhatsApp bot in pocket (silent)
5. Remember: **The three moments that win:** 47-second line, counter-card animation, final Bangla line
6. Remember: If anything breaks — you have the backup recording on USB, the offline JSON, and the cached investigation pages. Nothing can stop you from delivering the demo.

---

## POST-DEMO (while still at the event)

- [ ] Collect judge/attendee contact info
- [ ] Share your contact QR or card with anyone who expresses interest
- [ ] Note any questions you struggled with → improve QA_PREP.md for future
- [ ] Take a screenshot/photo of the demo running on the projector

---

## WHAT TO DO IF THINGS GO WRONG

| Problem | Immediate Action |
|---------|-----------------|
| URL paste fails (yt-dlp error) | Navigate to pre-cached investigation tab directly |
| SSE disconnects mid-stream | Navigate to investigation URL — cached result loads instantly |
| Claude API timeout | Pre-cached verdict in DB — investigation page shows it |
| Projector disconnects | Continue on laptop screen, pass it around if needed |
| Complete internet outage | Load offline JSON, narrate the evidence manually, play backup video from USB |
| Co-presenter sick | You know the whole script — you can run it solo |
| Judge asks hard question | Stop demo, answer directly, say "let me show you that" and navigate |

---

## DEMO DAY TIMELINE (June 12, 2026)

| Time | Action |
|------|--------|
| Morning | Arrive early. Set up laptop. Run T-1 hour checklist. |
| 30 min before slot | T-30 checklist. Final rehearsal. |
| 5 min before slot | T-5 checklist. Take position. |
| YOUR SLOT | 5-minute demo. |
| After demo | Q&A. Collect contacts. |
| Evening | Celebrate. You've earned it. |
