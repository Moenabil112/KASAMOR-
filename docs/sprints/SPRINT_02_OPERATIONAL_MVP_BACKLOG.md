# Sprint 02 — Operational MVP Backlog

**Builds on:** v0.1.0 MVP Foundation (`docs/releases/KASAMOR_MVP_FOUNDATION_v0_1_0.md`)
**Theme:** Move from a local-first, mock-driven MVP to an **operational MVP** — real
inputs, real retrieval, persisted decisions, and access control — without compromising
the data-governance guarantees established in v0.1.0.

> Guardrails (carry forward from v0.1.0): no public coordinates, no field-packet/raw
> media exposure, no gold-detection/mining-target language; AI assists, the House of
> Earth Trust decides; five-level sensitivity model enforced everywhere; coordinate
> redaction must remain green (`scripts/validate_safety.py`).

---

## Priority overview

| # | Epic | Priority | Depends on |
|---|---|---|---|
| 1 | Live AI provider adapter | P0 | — |
| 2 | Real media upload flow | P0 | — |
| 3 | Vector search adapter | P1 | 1 |
| 4 | Basic authentication | P0 | — |
| 5 | Persistent review decisions | P1 | 4 |
| 6 | Bilingual Arabic/English UI readiness | P1 | — |
| 7 | Field Packet ZIP upload | P1 | 2 |
| 8 | Offline/mobile capture preparation | P2 | 2, 7 |

---

## 1. Live AI provider adapter — P0
Replace deterministic mocks with real, provider-agnostic model calls behind the existing
`KASAMOR_AGENT_MODE` seam.

- [ ] Define a provider interface (`generate`, `embed`) with `mock` and `live` backends.
- [ ] Wire `KASAMOR_AGENT_MODE=live` + `KASAMOR_AI_PROVIDER` / key from `.env`.
- [ ] Implement at least one provider; keep `mock` as default and CI fallback.
- [ ] Enforce safety constraints from `agents/*.md` (no mineral-value claims; redaction-safe outputs).
- **Acceptance:** pipeline runs in both `mock` and `live`; identical output schema; mocks still work with no key.

## 2. Real media upload flow — P0
Accept real photos and voice notes (today only metadata exists).

- [ ] API upload endpoints for photo/voice tied to a Field Packet; store under `data/media/` (RESTRICTED).
- [ ] Object-storage seam (local disk now; signed-URL backend later).
- [ ] Internal console upload UI on the packet detail page.
- [ ] Strip/region-protect EXIF GPS on ingest; never expose raw media publicly.
- **Acceptance:** upload → metadata recorded → photo-quality/voice agents consume real files; `validate_safety.py` stays green.

## 3. Vector search adapter — P1
Replace keyword retrieval with embeddings while preserving sensitivity gating.

- [ ] Implement `VectorStoreAdapter` for `pgvector` and/or `Qdrant` (seam already present).
- [ ] Embedding job over `knowledge_chunks.jsonl`; select via `KASAMOR_VECTOR_BACKEND`.
- [ ] Keep `jsonl` keyword backend as default/offline fallback.
- [ ] Sensitivity filter applied **before** results return (no over-clearance leaks).
- **Acceptance:** semantic search returns relevant chunks; gating test still shows 0 leaks.

## 4. Basic authentication — P0
Introduce identity and roles for internal/partner surfaces.

- [ ] Auth on the API (session or token); login on the internal console.
- [ ] Roles: `contributor`, `reviewer`, `trust`, `partner` → map to sensitivity clearance.
- [ ] Public interface stays unauthenticated and PUBLIC-only.
- **Acceptance:** unauthenticated access cannot read INTERNAL+; clearance honored server-side.

## 5. Persistent review decisions — P1
Make House of Earth Trust decisions durable (currently demo-only).

- [ ] Persist `review_decision.schema.json` records via the API.
- [ ] Update Field Packet `review_status`/`review_decision`; audit trail (who/when/why).
- [ ] Console review buttons write through; reflect decided state.
- **Acceptance:** a decision survives reload and appears in reports.

## 6. Bilingual Arabic/English UI readiness — P1
Prepare the architecture for Arabic alongside English (English-first today).

- [ ] i18n framework + message catalogs; lift copy out of components/`content`.
- [ ] RTL layout support and a language switcher.
- [ ] Add `ar` content variant scaffolding (structure already shaped for it).
- **Acceptance:** both apps render EN and a stubbed AR locale with correct RTL.

## 7. Field Packet ZIP upload — P1
Allow a packet (notes + photos + voice) to be submitted as one ZIP.

- [ ] API endpoint accepting a ZIP; validate structure against `field_packet.schema.json`.
- [ ] Run Field Packet Intake agent for completeness/quality warnings.
- [ ] Route media to the upload flow (Epic 2); coordinate redaction on any embedded geo.
- **Acceptance:** valid ZIP → packet + media created; invalid ZIP → clear errors; no coord leakage.

## 8. Offline/mobile capture preparation — P2
Groundwork for rural, low-connectivity contributors.

- [ ] Define an offline capture data format (packet draft + queued media).
- [ ] Sync/queue API contract for deferred upload.
- [ ] PWA/offline-first spike for the capture surface.
- **Acceptance:** documented capture/sync contract + a working offline draft prototype.

---

## Cross-cutting (do alongside the epics)

- [ ] **CI workflow** — lint + `next build` (both apps) + `validate_safety.py` + API smoke on every PR.
- [ ] **Governance regression** — `validate_safety.py` wired into CI as a required check.
- [ ] **Docs** — update `docs/system-overview.md`, `docs/deployment.md`, governance as features land.

## Out of scope for Sprint 02
- Production multi-region deployment and per-region governance.
- Economic/impact analytics dashboards.
- Public operational mapping of any kind (permanently out of scope).
