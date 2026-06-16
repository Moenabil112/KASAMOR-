# KASAMOR — MVP Roadmap

This is the phase-by-phase plan the MVP foundation was built against, plus the
near-term path forward. The high-level summary lives in the root `ROADMAP.md`.

## Build phases (delivered)

### Phase 1 — Repository setup
Monorepo structure, 7 JSON Schemas, sample Field Packet / photo / voice data,
`.env.example`, `docker-compose.yml`, root README/ROADMAP.

### Phase 2 — Knowledge ingestion
`ingest_base_knowledge.py` (DOCX/MD/GeoJSON/PNG, stdlib only) →
`knowledge_chunks.jsonl`, `document_registry.json`, `knowledge_index_summary.md`.
Sensitivity-aware local retrieval in `rag-service`.

### Phase 3 — API
FastAPI with local JSON storage; sensitivity model; 8 MVP endpoints.

### Phase 4 — Agent mocks
6 agent specifications, deterministic mock orchestrator, media-processing mocks,
Markdown report generator, demo scripts.

### Phase 5 — Internal console
Next.js console: knowledge base, field packets, packet detail, review, reports.

### Phase 6 — Public interface
Next.js explainable interface: home + ecosystem + how-it-works + mvp + partners.

### Phase 7 — Test & report
End-to-end verification (ingestion → pipeline → report), build summary.

## Acceptance criteria (status)

1. Clean, structured repository — ✅
2. Package placed into `data/base-knowledge/` — ✅
3. Ingestion extracts + indexes — ✅ (23 docs, 176 chunks)
4. Knowledge chunks as JSONL — ✅
5. `/health` works — ✅
6. Knowledge summary returns — ✅
7. Sample Field Packet exists — ✅
8. Mock pipeline runs end-to-end — ✅
9. Markdown Field Packet report generated — ✅
10. Internal console shows summary + sample packet — ✅
11. Public interface explains without sensitive data — ✅
12. No old mistakes (no public target map, no R&D dump, no gold-detection claims) — ✅
13. Docs explain local run — ✅

## Next sprints

1. **Live AI** — provider-agnostic model calls behind `KASAMOR_AGENT_MODE=live`.
2. **Real media** — audio transcription + image quality vision.
3. **Vector search** — pgvector/Qdrant adapter replacing JSONL keyword retrieval.
4. **Database** — PostgreSQL + PostGIS for packets, media, geospatial queries.
5. **Auth & roles** — contributor / reviewer / trust / partner access control.
6. **Bilingual** — Arabic/English content pipeline + RTL UI.
7. **Mobile capture** — offline-first contributor client.
8. **Trust workflow** — full review audit trail and confidence gating.
9. **Region onboarding** — toolkit to bootstrap a new AOI responsibly.
