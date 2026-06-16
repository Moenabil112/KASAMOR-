# KASAMOR MVP Foundation — Release Notes

**Version:** v0.1.0 (MVP Foundation)
**Release type:** Local-first MVP baseline
**Merge commit:** `39bc093` (PR #1)
**Date:** 2026-06-16
**Recommended tag:** `v0.1.0-mvp-foundation`

> KASAMOR is a **Rural Mineral Intelligence Ecosystem** — a knowledge system that turns
> rural field knowledge (voice, photos, location, seasonal observation, sediment/rock
> documentation) into structured, sensitivity-governed intelligence, supported by AI and
> reviewed by the House of Earth Trust. It is **not** a gold-detection app, mining target
> map, public prospecting tool, or speculative mineral-claim platform.

---

## 1. What landed in `main`

The first functional, local-first MVP foundation — runs with **no API keys** and **no
database**. Merged via PR #1 (8 commits, 114 files, +8,878).

- Two connected-but-separate products: **Core System** (internal) and **Explainable
  Interface** (public).
- End-to-end knowledge flow: ZIP package → ingestion → RAG chunks → mock agent pipeline →
  House of Earth Trust review card → Markdown report.
- Five-level data sensitivity model enforced across all surfaces, with automatic
  coordinate redaction at ingestion.
- 13/13 acceptance criteria met; full validation suite passing from `main`.

## 2. Repository structure

```
kasamor-platform/
├── apps/
│   ├── public-interface/     # Next.js public explainable interface (5 pages)
│   └── internal-console/     # Next.js internal operating console (6 routes)
├── services/
│   ├── api/                  # FastAPI core API (local JSON, sensitivity model)
│   ├── rag-service/          # local-first retrieval + chunking + redaction seam
│   ├── agent-orchestrator/   # 6 mock agents + pipeline registry
│   ├── media-processing/     # mock photo-quality + voice-structuring
│   └── report-generator/     # Markdown field-packet + MVP summary reports
├── data/                     # local-first storage (knowledge, packets, outputs, geo*)
├── agents/                   # 6 provider-agnostic agent specifications
├── schemas/                  # 7 JSON schemas
├── docs/                     # overview, setup, deployment, governance, roadmap,
│                             # validation report, screenshots, releases, sprints
├── scripts/                  # ingest, mock pipeline, demo report, validate_safety
├── .env.example  docker-compose.yml  README.md  ROADMAP.md
```
`data/geo/` (raw GeoJSON/KML) is gitignored — restricted storage only.

## 3. System components

| Component | Tech | Notes |
|---|---|---|
| Knowledge ingestion | Python (stdlib) | DOCX/MD/GeoJSON/PNG → JSONL chunks + registry + summary; coordinate redaction |
| RAG retrieval | Python | sensitivity-aware keyword retrieval over JSONL; pgvector/Qdrant seam |
| Agent orchestrator | Python | 6 provider-agnostic mock agents; `KASAMOR_AGENT_MODE` seam |
| Media processing | Python | mock photo-quality + voice-structuring (no real vision/ASR) |
| Report generator | Python | Markdown field-packet + MVP summary reports |
| Core API | FastAPI + Pydantic | 8 endpoints, local JSON storage, 5-level sensitivity model |
| Public interface | Next.js 14 + TS + Tailwind | static, earth-tone, no maps |
| Internal console | Next.js 14 + TS + Tailwind | live-API wired, mock fallback |

## 4. Public interface summary

`apps/public-interface` — calm, earth-tone explainable site. **Fully static** (renders
from `content/site.ts`); makes **no API calls**, so it has no path to sensitive data.

- Pages: `/`, `/ecosystem`, `/how-it-works`, `/mvp`, `/partners`.
- The ~180 km² study area is shown as an **abstract scale, never a map**; no coordinates,
  no operational points.
- Positioning consistently "Rural Mineral Intelligence Ecosystem"; no gold-map /
  dashboard / prospecting language. `next build`: PASS.

## 5. Internal console summary

`apps/internal-console` — internal operating console reading **live API data** (graceful
mock fallback).

- Routes: `/`, `/knowledge-base`, `/field-packets`, `/field-packets/[id]`, `/review`,
  `/reports`.
- Location is shown as "RESTRICTED — not displayed"; knowledge base shows sensitivity
  breakdown (now 4 levels); review cards expose the 6 decision options; reports generate
  Markdown via the API. `next build`: PASS.

## 6. Knowledge ingestion summary

`scripts/ingest_base_knowledge.py` ingests the latest clean base knowledge package.

- **23 documents → 176 chunks.**
- Outputs: `knowledge_chunks.jsonl`, `document_registry.json`, `knowledge_index_summary.md`.
- Sensitivity distribution: `PARTNER 83 / INTERNAL 82 / RESTRICTED 10 / HOUSE_OF_EARTH_TRUST_ONLY 1`.
- All chunks carry schema-required fields; geospatial files indexed as RESTRICTED
  descriptors only.

## 7. Coordinate-redaction safety fix

Closes the medium validation finding (exact AOI coordinates in PARTNER/INTERNAL chunks).

- New `redact_coordinates()` detects decimal lat/lon pairs, `lat`/`lon` JSON fields,
  GeoJSON `coordinates` arrays, KML `<coordinates>`, `lookat_*` values, and AOI center
  references → `[RESTRICTED_COORDINATE]` / `[PROTECTED_GEOSPATIAL_REFERENCE]`.
- **16 references redacted**, **9 chunks reclassified** (8 → RESTRICTED, 1 →
  HOUSE_OF_EARTH_TRUST_ONLY).
- Raw GeoJSON/KML preserved only in gitignored `data/geo/`.
- **0 raw coordinates** remain in any PUBLIC/PARTNER/INTERNAL chunk.
- `scripts/validate_safety.py` enforces the guarantees on every run (all checks PASS).

## 8. Validation result (re-run from `main`)

| Check | Result |
|---|---|
| Ingestion | ✅ 23 docs → 176 chunks |
| `validate_safety.py` | ✅ ALL PASS (8 checks) |
| API endpoints | ✅ 10/10 (8 endpoints + 404 + 422) |
| Mock agent pipeline | ✅ 5/5 stages → report |
| `next build` public-interface | ✅ PASS |
| `next build` internal-console | ✅ PASS |

## 9. Known deferred items

- Live AI provider wiring (agents are deterministic mocks; `KASAMOR_AGENT_MODE=live` seam).
- Vector database (keyword-over-JSONL today; pgvector/Qdrant adapters deferred).
- PostgreSQL / PostGIS (local JSON storage in the MVP).
- Authentication / role-based access control.
- Real media transcription & image vision.
- Persistent console review decisions (demo-only).
- Bilingual Arabic/English UI (English-first; architecture prepared).
- Continuous integration (no CI workflow configured yet).

## 10. Recommended Sprint 02 scope

Operational MVP — see `docs/sprints/SPRINT_02_OPERATIONAL_MVP_BACKLOG.md`:

1. Live AI provider adapter (provider-agnostic).
2. Real media upload flow (photos/voice).
3. Vector search adapter (pgvector/Qdrant).
4. Basic authentication.
5. Persistent review decisions.
6. Bilingual Arabic/English UI readiness.
7. Field Packet ZIP upload.
8. Offline/mobile capture preparation.
