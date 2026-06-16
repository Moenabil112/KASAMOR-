# KASAMOR MVP — Validation Report

**Date:** 2026-06-16 (updated after coordinate-redaction fix)
**Scope:** Visual + functional validation, plus the coordinate-redaction hardening
requested after the first pass. No new product features added. Not merged.
**Branch:** `claude/tender-knuth-btb2uf`
**Environment:** API on `:8000`, public interface on `:3000`, internal console on
`:3001` (both Next.js apps served via `next build && next start`; console wired to
the live API).

---

## 1. Result summary

| Area | Result |
|---|---|
| Public interface review | ✅ Pass |
| Internal console review | ✅ Pass |
| API endpoint verification (8 endpoints) | ✅ Pass |
| RAG ingestion verification | ✅ Pass |
| Mock agent pipeline verification | ✅ Pass |
| Sensitivity gating verification | ✅ Pass (0 leaks) |
| Coordinate redaction verification | ✅ Pass (new) |
| Public safety scan | ✅ Pass |
| Positioning / language check | ✅ Pass |

**The medium-severity finding from the first pass (§10.1) is now RESOLVED.**
All eight `scripts/validate_safety.py` checks pass.

---

## 2. Coordinate-redaction fix (this update)

**Problem (first pass):** exact AOI center coordinates
(`14.59465389431194, 35.45663416544122`) appeared in 8 knowledge chunks
classified `PARTNER`/`INTERNAL`, contradicting the governance promise that raw
coordinates are RESTRICTED.

**Fix:** the ingestion pipeline now redacts coordinate content from chunk text and
elevates sensitivity automatically.

- New utility `redact_coordinates()` in `scripts/ingest_base_knowledge.py` detects
  decimal lat/lon pairs, `"lat"/"lon"/"latitude"/"longitude"` JSON fields, GeoJSON
  `"coordinates"` arrays, KML `<coordinates>` strings, `lookat_*` values, and exact
  AOI center references.
- Matches are replaced with `[RESTRICTED_COORDINATE]` or
  `[PROTECTED_GEOSPATIAL_REFERENCE]`.
- Any chunk with a redaction is elevated to `RESTRICTED`, or
  `HOUSE_OF_EARTH_TRUST_ONLY` when linked to private expert/evidence context.
- Original GeoJSON/KML files are copied to restricted local storage
  (`data/geo/`, gitignored) and never committed/exposed.
- New `scripts/validate_safety.py` enforces the guarantees repeatably.

**Outcome of re-ingestion (23 docs / 176 chunks):**

- **16** coordinate references redacted across **9** chunks reclassified.
- Sensitivity distribution moved from
  `PARTNER 87 / INTERNAL 87 / RESTRICTED 2`
  to **`PARTNER 83 / INTERNAL 82 / RESTRICTED 10 / HOUSE_OF_EARTH_TRUST_ONLY 1`**.
- **0** raw coordinates remain in **any** chunk at **any** level (placeholders only).

Reclassified chunks (all previously PARTNER/INTERNAL):

| Chunk | Source | New level |
|---|---|---|
| KSM-KB-0067 | 03 Field Intelligence Protocol | RESTRICTED |
| KSM-KB-0069/0072/0091/0094 | 04 MVP Study Area | RESTRICTED |
| KSM-KB-0100 | 05 Technical Blueprint ("expert evidence") | HOUSE_OF_EARTH_TRUST_ONLY |
| KSM-KB-0106/0107 | 05 Technical Blueprint | RESTRICTED |
| KSM-KB-0144 | 10 Field Packet Templates | RESTRICTED |

Generalized study-area language (e.g. "approximately 180 km² … Center:
`[RESTRICTED_COORDINATE]`") is preserved; only the coordinate values are removed.

---

## 3. Public interface review

All five pages render correctly with the intended earth-tone, calm design (deep
green / sand / charcoal / muted gold), strong typography, light abstract diagrams.
No maps, no operational visuals, no gold-rush imagery.

| Page | Screenshot | Notes |
|---|---|---|
| Home | `public/01-homepage.png` | Hero + all 10 narrative sections + footer safety note. |
| Ecosystem | `public/02-ecosystem.png` | Five-layer model, field-intelligence chips, Trust section. |
| How it works | `public/03-how-it-works.png` | Capture→Replicate flow + "AI assists — it never decides". |
| MVP | `public/04-mvp.png` | Abstract ~180 km² circle, explicitly "not a map". |
| Partners | `public/05-partners.png` | Four partner audiences + working principles. |

- "Rural Mineral Intelligence" present on every page.
- Footer on every page states the non-exposure commitment.
- Fully static (renders from `content/site.ts`); **no API calls**, so no path to
  sensitive data. Public screenshots are unchanged by the fix.

## 4. Internal console review

All six routes render and read **live API data**. The knowledge base now correctly
shows **4 sensitivity levels** post-fix (`02-knowledge-base.png`).

| Page | Screenshot | Notes |
|---|---|---|
| Overview | `internal-console/01-overview.png` | Live counts + pipeline description. |
| Knowledge base | `internal-console/02-knowledge-base.png` | **Updated** — PARTNER 83 / INTERNAL 82 / RESTRICTED 10 / HOET 1. |
| Knowledge search | `internal-console/08-knowledge-search.png` | **Updated** — live retrieval with sensitivity badges. |
| Field packets | `internal-console/03-field-packets.png` | "Coordinates are RESTRICTED and never shown here". |
| Packet detail | `internal-console/04-field-packet-detail.png` | Location shows "RESTRICTED — not displayed". |
| Review | `internal-console/05-review.png` | Trust review cards, all 6 decision buttons. |
| Reports | `internal-console/06-reports.png` | Selector + generate. |
| Reports (generated) | `internal-console/07-reports-generated.png` | Live Markdown incl. sensitivity note. |

## 5. API endpoint verification (live, post-fix)

| Endpoint | Result |
|---|---|
| `GET /health` | 200 |
| `GET /knowledge/summary` | 200 (176 chunks; 4 sensitivity levels) |
| `POST /knowledge/search` | 200 |
| `GET /field-packets` | 200 (2) |
| `GET /field-packets/{id}` | 200 |
| `GET /field-packets/KSM-FP-9999` | 404 (correct) |
| `POST /agents/run/mock` | 200 (5 steps) |
| `POST /reports/field-packet/{id}` | 200 |

`top_k > 25` → 422 (Pydantic bound enforced).

## 6. RAG ingestion verification

- Outputs regenerated: `knowledge_chunks.jsonl`, `document_registry.json`,
  `knowledge_index_summary.md`.
- **23 documents → 176 chunks.** All chunks carry the schema-required fields.
- Registry now records `redacted_coordinate_refs` (16) and `reclassified_chunks` (9).
- **0** raw coordinates in chunk content (verified across all levels).

## 7. Mock agent pipeline verification

`scripts/run_mock_agent_pipeline.py` and `POST /agents/run/mock` run the full
five-stage pipeline and write `data/outputs/reports/KSM-FP-0001_report.md`. Mode
`mock`, no keys. AI limitations and `needs_human_review` present in every output.

## 8. Sensitivity gating verification (post-fix)

Query: "center latitude longitude coordinates gps geojson" (designed to surface any
coordinate content):

| Clearance | Results | Over-clearance leaks | Raw coords in snippet |
|---|---|---|---|
| PUBLIC | 0 | 0 | 0 |
| PARTNER | 24 | 0 | 0 |
| INTERNAL | 25 | 0 | 0 |

No caller receives chunks above clearance, and **no coordinate appears in any
returned snippet**.

## 9. Coordinate-redaction validation (`scripts/validate_safety.py`)

```
[PASS] 0 exact coordinates in PUBLIC chunks
[PASS] 0 exact coordinates in PARTNER chunks
[PASS] 0 exact coordinates in INTERNAL chunks
[PASS] all raw-coordinate content is restricted (none in PUBLIC/PARTNER/INTERNAL)
[PASS] redaction applied (refs=16, chunks_with_placeholder=9)
[PASS] geospatial-derived chunks contain no raw coordinates
[PASS] public interface source: no coordinates or field-packet data
[PASS] restricted geospatial originals preserved locally only (2 file(s), gitignored)
RESULT: ALL PASS
```

## 10. Public safety scan (served HTML)

Scan of the live-served public HTML for all five pages:

- Exact coordinates / `lookat_`: **none**.
- Field-packet / contributor / photo / voice ids: **none**.
- GeoJSON / KML / FeatureCollection references: **none**.
- Forbidden terms: only `"target map"` — exclusively in the negation "not a target
  map". No gold-detection, prospecting, guaranteed, reserve-estimate, or
  extraction-instruction language.

## 11. Positioning / language check

- "Rural Mineral Intelligence" present on all public pages.
- No "mining dashboard", "prospecting tool", or "gold map" anywhere.
- KASAMOR consistently framed as a **Rural Mineral Intelligence Ecosystem** with
  the House of Earth Trust as the review/protection layer — not a gold map, mining
  dashboard, or public prospecting tool.

## 12. Issues

### 12.1 (RESOLVED) Exact AOI coordinates in PARTNER/INTERNAL chunks
Fixed by automatic coordinate redaction + sensitivity elevation at ingestion
(§2). Re-verified: 0 raw coordinates in any PUBLIC/PARTNER/INTERNAL chunk.

### 12.2 (LOW / INFO) `top_k > 25` returns 422
Not a bug — Pydantic bound. Documented for consumers.

### 12.3 (LOW) Review decisions are not persisted
MVP by design (noted in UI).

## 13. Known limitations (unchanged)

- AI agents, image vision, voice transcription are deterministic **mocks**.
- Retrieval is keyword-based over JSONL (no vector DB).
- Storage is local JSON (no PostgreSQL/PostGIS).
- No authentication / role-based access control.
- Console review decisions are demo-only.

## 14. Acceptance criteria

**13 / 13 still met** (see `docs/mvp-roadmap.md`). The redaction fix strengthens
criteria 11–12 (no sensitive data exposed) without changing any feature behaviour.

## 15. Generated screenshots

```
docs/screenshots/public/
  01-homepage.png  02-ecosystem.png  03-how-it-works.png  04-mvp.png  05-partners.png
docs/screenshots/internal-console/
  01-overview.png  02-knowledge-base.png*  03-field-packets.png  04-field-packet-detail.png
  05-review.png  06-reports.png  07-reports-generated.png  08-knowledge-search.png*
  (* regenerated after the redaction fix)
```

**Verdict:** The MVP is visually and functionally sound and safe for public
exposure. The medium-severity coordinate finding is resolved and enforced by an
automated check. **The PR is ready to open pending your review of this report.**
