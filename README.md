# KASAMOR — Rural Mineral Intelligence Ecosystem

> KASAMOR is an AI-supported **rural mineral intelligence ecosystem** that converts
> local knowledge, field evidence, mobile photos, voice notes, geospatial data, and
> expert review into practical, responsible guidance for understanding natural mineral
> resources in remote environments — reviewed and protected by the **House of Earth Trust**.

KASAMOR is **not** a gold-detection app, **not** a mining target map, **not** a public
prospecting platform, and **not** a speculative mineral-claim system. It is a knowledge
system for **responsible resource understanding** that is **repeatable across remote regions**.

---

## What this repository contains

This is a local-first MVP monorepo with two connected but separate products:

| Product | Path | Purpose |
|---|---|---|
| **A — Core System** (internal) | `apps/internal-console`, `services/*` | Base-knowledge ingestion, RAG-ready knowledge base, Field Packet intake, photo/voice/location handling, mock AI-agent workflow, House of Earth Trust review, report-ready outputs. |
| **B — Explainable Interface** (public) | `apps/public-interface` | Calmly explains what KASAMOR is, who it serves, how the ecosystem works — **without exposing sensitive coordinates or field data**. |

```
kasamor-platform/
├── apps/                # Next.js front-ends (public-interface, internal-console)
├── services/            # Python services (api, rag-service, agent-orchestrator,
│                        #                   media-processing, report-generator)
├── data/                # Local-first storage (base/extracted knowledge, packets, outputs)
├── agents/              # 6 provider-agnostic AI agent specifications
├── schemas/             # 7 JSON Schemas (field packet, photo, voice, etc.)
├── docs/                # System overview, setup, deployment, governance, roadmap
├── scripts/             # Ingestion + demo pipeline + report export
├── .env.example
├── docker-compose.yml
└── ROADMAP.md
```

---

## Source of truth

The single source of truth is the **latest clean base knowledge package**:
`KASAMOR_Latest_Base_Knowledge_Package_Clean.zip` (13 core documents, 2 geospatial
reference files, 6 supporting figures). Legacy HTML pages, old dashboards, old maps,
and previous skeletons are intentionally **not** used.

---

## Quick start (local, no API keys, no database)

### 1. Ingest the base knowledge package
```bash
python3 scripts/ingest_base_knowledge.py \
  --zip /path/to/KASAMOR_Latest_Base_Knowledge_Package_Clean.zip
```
Generates:
- `data/extracted-knowledge/knowledge_chunks.jsonl`
- `data/extracted-knowledge/document_registry.json`
- `data/extracted-knowledge/knowledge_index_summary.md`

### 2. Run the API (FastAPI)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload --port 8000
# Health:   http://localhost:8000/health
# Summary:  http://localhost:8000/knowledge/summary
```

### 3. Run the mock agent pipeline (end-to-end, no keys needed)
```bash
python3 scripts/run_mock_agent_pipeline.py
# -> data/outputs/reports/KSM-FP-0001_report.md
```

### 4. Run the internal console
```bash
cd apps/internal-console && npm install && npm run dev   # http://localhost:3001
```

### 5. Run the public interface
```bash
cd apps/public-interface && npm install && npm run dev    # http://localhost:3000
```

> The front-ends gracefully fall back to bundled mock data when the API is not running,
> so each app can be demoed independently.

---

## How the pieces connect

```
ZIP package ──ingest──▶ knowledge_chunks.jsonl ──▶ rag-service (mock retrieval)
                                                         │
Field Packet ─┐                                          ▼
Photos ───────┼─▶ media-processing ─▶ agent-orchestrator (6 mock agents)
Voice notes ──┘                              │
                                             ▼
                              House of Earth Trust review card
                                             │
                                             ▼
                              report-generator ─▶ Markdown report
```

The **API service** exposes all of this over HTTP; both front-ends read from it.

---

## What is **not** included yet

- Real AI model calls (agents run as deterministic **mocks**; provider-agnostic interfaces are in place).
- Real audio transcription / image vision (mock metadata logic only).
- Vector database (retrieval is over local JSONL; pgvector/Qdrant are placeholder adapters).
- PostgreSQL/PostGIS (placeholders only; MVP uses local JSON files).
- Authentication, multi-tenant access control, and production hardening.
- Any public operational map with real coordinates (intentionally excluded for safety).

See `ROADMAP.md` and `docs/mvp-roadmap.md` for what comes next.

---

## Safety & governance at a glance

Five sensitivity levels gate all data: `PUBLIC`, `PARTNER`, `INTERNAL`, `RESTRICTED`,
`HOUSE_OF_EARTH_TRUST_ONLY`. The public interface may only render `PUBLIC` (and
carefully selected `PARTNER`) content. Raw coordinates, photos, voice notes, exact
field packets, and community-sensitive data are **never** exposed publicly.
See `docs/data-governance.md`.
