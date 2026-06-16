# KASAMOR Platform — Roadmap

This roadmap tracks the MVP foundation and the path beyond it. The detailed,
phase-by-phase MVP plan lives in `docs/mvp-roadmap.md`; this file is the
high-level summary.

## ✅ MVP Foundation (this build)

- [x] Clean monorepo structure (apps / services / data / agents / schemas / docs / scripts)
- [x] 7 JSON Schemas (field packet, photo, voice, observation, review, knowledge chunk, report)
- [x] Base-knowledge ingestion (DOCX/MD/GeoJSON/PNG → JSONL chunks + registry + summary)
- [x] Five-level sensitivity model + data-governance documentation
- [x] FastAPI service with local JSON storage (8 MVP endpoints)
- [x] 6 provider-agnostic agent specifications + deterministic mock execution
- [x] Mock agent pipeline (intake → photo → voice → fusion → review card → report)
- [x] Markdown Field Packet report generator
- [x] Internal console (knowledge base, field packets, detail, review, reports)
- [x] Public explainable interface (5 pages, earth-tone calm design, no sensitive data)

## 🔜 Next sprint candidates

- [ ] Wire real, provider-agnostic AI model calls (`KASAMOR_AGENT_MODE=live`)
- [ ] Real audio transcription + image quality vision models
- [ ] Replace JSONL retrieval with pgvector / Qdrant adapter
- [ ] PostgreSQL + PostGIS for packets, media, and geospatial queries
- [ ] Authentication + role-based access (contributor / reviewer / trust / partner)
- [ ] Bilingual (Arabic/English) content pipeline and RTL UI
- [ ] Offline-first mobile capture client for rural contributors
- [ ] House of Earth Trust review workflow with audit trail
- [ ] Repeatable region-onboarding toolkit (new AOI bootstrap)

## 🌍 Long-term

- Multi-region deployment with per-region governance.
- Knowledge-based rural livelihood programs and impact measurement.
- Academic, technical, and development-partner integrations.
