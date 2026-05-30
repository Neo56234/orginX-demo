# OriginX Execution Memory & State

## Current Phase: Phase 4 (Final Polish & Bug Fixes)
- The core OriginX pipeline (Fast-Track pHash and LLM Adjudicator) has been implemented and tested.
- Next.js frontend has SSE event handling mapped to agent swarm UI.
- Known critical bugs (backend timeouts, SSE mapping errors, etc.) from `BUG_REPORT.md` are actively being resolved for the demo.
- Dev Psyche and SatelliteOrbs are finalized for daily.dev submission.
- Focus is strictly on ensuring the presentation demo (Fast-Track verification + Swarm execution) operates reliably without crashes.

## Important Lessons & Conventions
- **SSE Payload Mapping:** Frontend components MUST safely handle missing keys in the SSE `progress` and `findings` payloads to avoid UI crashes.
- **RQ Worker Timeouts:** Video processing takes longer than default RQ timeouts. Always ensure long-running worker tasks (like `ffmpeg` keyframe extraction and CLIP embeddings) have an extended `timeout` (e.g., `job_timeout="10m"`).
- **Fast-Track Priority:** If a visual pHash match is found early in the database, bypass the LLM Adjudicator orchestration entirely to save execution time (reduces 60s → 2s).
- **Prompt Reliability:** Always use `json_mode` on Claude's API to ensure the `Adjudicator` returns syntactically valid JSON for verdict serialization.

## Next Steps / Active Todos
- [ ] Record YouTube Demo Video (10 points remaining for Hackathon).
- [ ] Submit Live Vercel Link.
- [ ] Set GitHub repository to public (if not already done).
- [ ] Review `DEMO_SCRIPT.md` to ensure a reproducible, crash-free presentation path.
