# KASAMOR — System Overview

KASAMOR is a **Rural Mineral Intelligence Ecosystem**: it turns scattered local
field knowledge into structured, sensitivity-governed intelligence, supported by AI
and reviewed by the House of Earth Trust.

## Two products

- **Product A — Core System** (internal): ingestion, knowledge base, Field Packet
  intake, media handling, agent workflow, review, reports. Lives in
  `services/*` and `apps/internal-console`.
- **Product B — Explainable Interface** (public): explains the ecosystem safely.
  Lives in `apps/public-interface`.

## Architecture

```
                ┌────────────────────────────────────────────┐
  ZIP package ─▶│ ingest_base_knowledge.py                    │
                │   → knowledge_chunks.jsonl (+ registry,      │
                │     index summary)                           │
                └───────────────┬────────────────────────────┘
                                │
                       rag-service/retrieval.py (sensitivity-aware)
                                │
 Field Packet ─┐                ▼
 Photos ───────┼─▶ media-processing ─▶ agent-orchestrator (6 mock agents)
 Voice notes ──┘    (photo_quality,        intake → photo → voice →
                     voice_metadata)        fusion → trust review card
                                │
                                ▼
                     report-generator → Markdown report
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                                ▼
  services/api (FastAPI, local JSON)              data/outputs/reports
        │
   ┌────┴─────────────┐
   ▼                  ▼
 internal-console   public-interface   (Next.js)
```

## Components

| Layer | Tech | Notes |
|---|---|---|
| Ingestion | Python (stdlib only) | DOCX/MD/GeoJSON/PNG → JSONL chunks. |
| RAG | Python | Keyword retrieval over JSONL; pgvector/Qdrant deferred. |
| Agents | Python | 6 provider-agnostic specs; deterministic mock execution. |
| Media | Python | Mock photo-quality + voice-structuring (no real vision/ASR). |
| Reports | Python | Markdown Field Packet + MVP summary reports. |
| API | FastAPI + Pydantic | Local JSON storage; 8 MVP endpoints. |
| Front-ends | Next.js 14 + TS + Tailwind | Internal console + public interface. |

## Sensitivity model

Five levels gate all data (see `data-governance.md`). The public interface renders
PUBLIC content only; raw coordinates, photos, voice, and identities never leave the
internal boundary.

## What is mock vs real

Mock (MVP): AI agents, photo vision, voice transcription, vector search.
Real: ingestion, chunking, retrieval scoring, API, storage, reports, front-ends.
