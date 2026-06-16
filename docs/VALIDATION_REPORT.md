# KASAMOR MVP — Validation Report

**Date:** 2026-06-16
**Scope:** Visual + functional validation only. No new features added. Not merged.
**Branch:** `claude/tender-knuth-btb2uf`
**Environment:** API on `:8000`, public interface on `:3000`, internal console on `:3001`
(both Next.js apps served via `next build && next start`, console wired to the live API).

---

## 1. Result summary

| Area | Result |
|---|---|
| Public interface review | ✅ Pass |
| Internal console review | ✅ Pass |
| API endpoint verification (8 endpoints) | ✅ Pass |
| RAG ingestion verification | ✅ Pass (⚠ 1 governance note) |
| Mock agent pipeline verification | ✅ Pass |
| Sensitivity gating verification | ✅ Pass (0 leaks) |
| Public safety scan | ✅ Pass (no public exposure) |
| Positioning / language check | ✅ Pass |

**One medium-severity finding** (latent, not a public leak): exact AOI center
coordinates are embedded in 8 knowledge chunks classified `PARTNER`/`INTERNAL`.
See §10. Recommended to fix before PR.

---

## 2. Public interface review

All five pages render correctly with the intended earth-tone, calm design
(deep green / sand / charcoal / muted gold), strong typography, and light abstract
diagrams. No maps, no operational visuals, no gold-rush imagery.

| Page | Screenshot | Notes |
|---|---|---|
| Home | `public/01-homepage.png` | Hero + all 10 narrative sections + footer safety note. |
| Ecosystem | `public/02-ecosystem.png` | Five-layer model, field-intelligence chips, Trust section. |
| How it works | `public/03-how-it-works.png` | Capture→Replicate flow + "AI assists — it never decides". |
| MVP | `public/04-mvp.png` | Abstract ~180 km² circle, explicitly "not a map". |
| Partners | `public/05-partners.png` | Four partner audiences + working principles. |

- Positioning phrase **"Rural Mineral Intelligence"** present on every page
  (home ×8, others ×4).
- Footer on every page states the non-exposure commitment.
- The interface is **fully static** (renders from `content/site.ts`); it makes **no
  API calls**, so it has no path to sensitive data.

## 3. Internal console review

All six routes render and the console reads **live API data** (overview shows
"Data source: live API", 23 docs / 176 chunks / 2 packets / 2 pending).

| Page | Screenshot | Notes |
|---|---|---|
| Overview | `internal-console/01-overview.png` | Live counts + pipeline description. |
| Knowledge base | `internal-console/02-knowledge-base.png` | Domain + sensitivity breakdowns. |
| Knowledge search | `internal-console/08-knowledge-search.png` | Live retrieval with sensitivity badges. |
| Field packets | `internal-console/03-field-packets.png` | Two packets; "Coordinates are RESTRICTED and never shown here". |
| Packet detail | `internal-console/04-field-packet-detail.png` | **Location shows "RESTRICTED — not displayed"** despite stored lat/lon. |
| Review | `internal-console/05-review.png` | Trust review cards, all 6 decision buttons, AI-limitations note. |
| Reports | `internal-console/06-reports.png` | Selector + generate. |
| Reports (generated) | `internal-console/07-reports-generated.png` | Live-generated Markdown incl. sensitivity note. |

Functional checks performed in-browser: knowledge search executes and returns
results; "Generate report" calls the live API and renders Markdown; review decision
buttons are interactive.

## 4. API endpoint verification

Tested against the live server (`http://localhost:8000`):

| Endpoint | Result |
|---|---|
| `GET /health` | 200 |
| `GET /knowledge/summary` | 200 (176 chunks) |
| `POST /knowledge/search` | 200 |
| `GET /field-packets` | 200 (2) |
| `GET /field-packets/{id}` | 200 |
| `GET /field-packets/KSM-FP-9999` | 404 (correct) |
| `POST /agents/run/mock` | 200 (5 steps) |
| `POST /reports/field-packet/{id}` | 200 |

Input validation confirmed: `top_k > 25` is rejected with **422** (Pydantic bound),
i.e. the API guards against oversized requests.

## 5. RAG ingestion verification

- Outputs present: `knowledge_chunks.jsonl`, `document_registry.json`,
  `knowledge_index_summary.md`.
- **23 documents → 176 chunks.**
- All chunks carry the schema-required fields
  (`chunk_id`, `source_file`, `content`, `sensitivity_level`, `knowledge_domain`).
- Sensitivity distribution: `PARTNER` 87 · `INTERNAL` 87 · `RESTRICTED` 2.
- ⚠ 8 chunks contain coordinate-like numbers carried over from the source DOCX
  prose — see §10.

## 6. Mock agent pipeline verification

`scripts/run_mock_agent_pipeline.py` and `POST /agents/run/mock` both run the full
five-stage pipeline (intake → photo quality → voice-to-knowledge → fusion → Trust
review card) and produce a Markdown report at
`data/outputs/reports/KSM-FP-0001_report.md`. Mode reported as `mock`; no API keys
required. AI limitations and `needs_human_review` are present in every output.

## 7. Sensitivity gating verification

Search executed at each clearance with an aggressive query
("trust governance field gold sediment"):

| Clearance | Results | Over-clearance leaks |
|---|---|---|
| PUBLIC | 0 | 0 |
| PARTNER | 25 | 0 |
| INTERNAL | 25 | 0 |

A caller never receives chunks above their clearance. PUBLIC returns **0** because
there are **no PUBLIC chunks** — a fail-safe default.

## 8. Public safety scan

Scan of the **live-served public HTML** for all five pages:

- Exact coordinates (`35.45x` / `14.59x` / `lookat_`): **none**.
- Field-packet / contributor / photo / voice ids: **none**.
- GeoJSON / KML / FeatureCollection references: **none**.
- Forbidden terms: only `"target map"` appears — exclusively in the safety negation
  **"not a target map"** (verified in context). No gold-detection, prospecting,
  guaranteed, reserve-estimate, or extraction-instruction language.

## 9. Positioning / language check

- "Rural Mineral Intelligence" present on all public pages.
- No "mining dashboard", "prospecting tool", or "gold map" anywhere.
- Narrative consistently frames KASAMOR as a **Rural Mineral Intelligence
  Ecosystem** with the House of Earth Trust as the review/protection layer — not a
  gold map, mining dashboard, or public prospecting tool.

## 10. Issues found

### 10.1 (MEDIUM) Exact AOI coordinates embedded in PARTNER/INTERNAL chunks
The precise study-area center `14.59465389431194, 35.45663416544122` (and JSON
samples containing it) appears in **8 chunks**:

- `KSM-KB-0069/0072/0091/0094` — source `04_..._MVP_Study_Area...docx` — **PARTNER**
- `KSM-KB-0100/0106/0107` — source `05_..._Technical_AI_Agent...docx` — **INTERNAL**
- `KSM-KB-0144` — source `10_..._Field_Packet_Templates...docx` — **INTERNAL**

The ingestion classifies a chunk by its **source document's default sensitivity**.
Geospatial *files* are correctly downgraded to RESTRICTED descriptors, but
coordinates written **in prose / sample JSON inside the DOCX bodies** inherit the
document default (PARTNER for doc 04).

**Impact today:** none publicly. The public interface has no API path, PUBLIC
clearance returns 0 chunks, and the console hides location. **Latent risk:** the
data-governance policy promises raw coordinates are RESTRICTED; a future
PARTNER-tier surface could surface these.

**Severity:** Medium (governance/defense-in-depth, not an active public leak).

### 10.2 (LOW / INFO) `top_k > 25` returns 422
Not a bug — Pydantic correctly enforces the bound. Documented here so consumers
set `top_k ≤ 25`.

### 10.3 (LOW) Review decisions are not persisted
By design for the MVP (noted in the UI). Listed for completeness.

## 11. Known limitations (unchanged from build)

- AI agents, image vision, and voice transcription are deterministic **mocks**.
- Retrieval is keyword-based over JSONL (no embeddings / vector DB).
- Storage is local JSON (no PostgreSQL/PostGIS).
- No authentication / role-based access control.
- Console review decisions are demo-only (not persisted).

## 12. Recommended fixes before PR

1. **(Medium) Coordinate guard in ingestion** — detect lat/lon patterns in chunk
   `content` and either (a) redact them, or (b) force-elevate the chunk to
   `RESTRICTED`, regardless of the source document default. This closes the gap in
   §10.1 and makes the governance promise true by construction. *(Deferred — would
   be a code change; flagged for approval, not done in this validation pass.)*
2. **(Low) Document the `top_k ≤ 25` bound** in `services/api/README.md` and the
   console search hint.
3. **(Optional) Add `data/outputs/` to validation artifacts** or keep gitignored —
   confirm intended behaviour before PR.

## 13. Generated screenshots

```
docs/screenshots/public/
  01-homepage.png
  02-ecosystem.png
  03-how-it-works.png
  04-mvp.png
  05-partners.png
docs/screenshots/internal-console/
  01-overview.png
  02-knowledge-base.png
  03-field-packets.png
  04-field-packet-detail.png
  05-review.png
  06-reports.png
  07-reports-generated.png      (functional: live Markdown report)
  08-knowledge-search.png       (functional: live retrieval results)
```

**Verdict:** The MVP is visually and functionally sound and safe for public
exposure as built. One medium-severity governance hardening (§10.1) is recommended
before opening the PR.
