# Sprint 02 — Task 1: CI Foundation Notes

**Branch:** `feature/sprint-02-ci-foundation`
**Scope:** Add a GitHub Actions CI workflow that enforces the KASAMOR MVP
data-governance guarantees and verifies the Python services + both Next.js apps.
**No product features added** — this task is CI/validation infrastructure only.

---

## What the CI checks

Workflow: `.github/workflows/ci.yml` (runs on every pull request and on push to
`main`). Three parallel jobs:

### 1. `python-validation`
- Installs `services/api/requirements.txt` (Python 3.11).
- `scripts/validate_safety.py` — coordinate-redaction guarantee (see below).
- `scripts/validate_api.py` — FastAPI import/startup + OpenAPI route validation.
- `scripts/run_mock_agent_pipeline.py` — full 5-stage mock pipeline.
- Asserts `data/outputs/reports/KSM-FP-0001_report.md` is generated.

### 2. `public-interface`
- `npm ci` + `npm run build` (Node 20) for `apps/public-interface`.
- Starts the built server, waits for readiness, runs
  `scripts/scan_public_html.py`, then stops the server.
- The scan **fails CI** if any served page contains exact coordinates,
  GeoJSON/KML references, field-packet data, or forbidden positioning language
  (gold-detection / mining-target / prospecting). The "not a target map" negation
  is explicitly allowed.

### 3. `internal-console`
- `npm ci` + `npm run build` (Node 20) for `apps/internal-console`.

### CI fails if (safety requirement)
- Exact coordinates appear in PUBLIC/PARTNER/INTERNAL chunks **or** the redaction
  mechanism regresses (caught by the self-test even without the corpus).
- Public served HTML contains coordinates, GeoJSON, field-packet data, or
  forbidden language.
- The mock agent pipeline fails or the report is not produced.
- Either Next.js app fails to build.
- The API app/routes fail to import or the OpenAPI schema fails to build.

---

## How to run the checks locally

```bash
# Python (from repo root)
pip install -r services/api/requirements.txt
python3 scripts/validate_safety.py
python3 scripts/validate_api.py
python3 scripts/run_mock_agent_pipeline.py
test -f data/outputs/reports/KSM-FP-0001_report.md && echo "report OK"

# Public interface build + served-HTML safety scan (atomic: start -> scan -> stop)
cd apps/public-interface && npm ci && npm run build
( npm run start & SRV=$!; \
  for i in $(seq 1 45); do curl -sf -o /dev/null http://localhost:3000/ && break; sleep 1; done; \
  python3 ../../scripts/scan_public_html.py http://localhost:3000; ST=$?; \
  kill $SRV 2>/dev/null; exit $ST )

# Internal console build
cd apps/internal-console && npm ci && npm run build
```

---

## Known local limitations

- **Background servers can be reclaimed between separate shell invocations** in
  the remote dev environment. Start → wait → scan → stop must therefore run in a
  **single** shell command (as above and in the CI step). Splitting them across
  steps can leave the scanner unable to connect (it then fails closed, which is
  correct but not what you want locally). GitHub Actions runs each job step in a
  persistent shell, so the CI start/scan/stop step is stable there.
- `scripts/scan_public_html.py` **fails closed**: if it cannot reach the server,
  it reports FAIL. This is intentional — an unreachable server must not pass.
- `validate_api.py` is **import-level only** (no live HTTP server, no extra HTTP
  client dependency). It imports the app, imports every route module, confirms
  the expected endpoints are registered, and builds the OpenAPI schema.

---

## Why extracted-knowledge artifacts are regenerated, not committed

`data/extracted-knowledge/` (`knowledge_chunks.jsonl`, `document_registry.json`,
`knowledge_index_summary.md`) and `data/geo/` (raw GeoJSON/KML) are **gitignored
by design**:

- They are **build artifacts** derived from the base knowledge package, which is
  not stored in the repo.
- The raw geospatial files and any chunk content contain coordinates that must
  live only in restricted storage — committing them would defeat the governance
  model.

They are regenerated locally with:
```bash
python3 scripts/ingest_base_knowledge.py --zip <KASAMOR_Latest_Base_Knowledge_Package_Clean.zip>
```
CI therefore runs **without** these artifacts. The safety validator handles this
(see below) and the workflow does not commit or expect generated artifacts.

---

## How coordinate-redaction safety is enforced

`scripts/validate_safety.py` enforces the guarantee in two complementary ways:

1. **Redaction self-test (always runs, no corpus needed).** It loads
   `redact_coordinates()` / `elevated_level_for()` from
   `scripts/ingest_base_knowledge.py` and feeds them known coordinate forms
   (decimal lat/lon pair, `lat`/`lon` JSON fields, GeoJSON `coordinates` array,
   KML `<coordinates>`, "latitude/longitude" prose). It asserts every form is
   redacted (0 raw coordinates remain) and that coordinate-bearing chunks are
   elevated to `RESTRICTED` (or `HOUSE_OF_EARTH_TRUST_ONLY` for expert/evidence
   context). If redaction regresses, CI fails — even on a fresh checkout with no
   chunks.

2. **Chunk-level checks (run when the corpus is present).** When
   `knowledge_chunks.jsonl` exists (i.e. after local ingestion), it additionally
   asserts 0 raw coordinates in any PUBLIC/PARTNER/INTERNAL chunk, that any
   coordinate content is restricted, that redaction placeholders are present, and
   that geospatial-typed chunks are coordinate-free.

Plus a **public-interface source scan** (no coordinates / field-packet data in
`apps/public-interface` source) and a confirmation that raw geospatial originals
live only in gitignored restricted storage. The served-HTML scan in the
`public-interface` job covers the rendered output.

---

## Local validation result (this branch)

| Check | Result |
|---|---|
| `validate_safety.py` (with chunks) | ✅ ALL PASS |
| `validate_safety.py` (no chunks / CI mode) | ✅ ALL PASS (self-test) |
| `validate_api.py` | ✅ ALL PASS (7 routes, OpenAPI 8 paths) |
| `run_mock_agent_pipeline.py` | ✅ report generated (2,337 bytes) |
| `scan_public_html.py` (live server) | ✅ PASS (5 pages clean) |
| `next build` public-interface | ✅ PASS |
| `next build` internal-console | ✅ PASS |
