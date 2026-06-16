# KASAMOR — Local Setup

The MVP is **local-first**: no database, no API keys, no cloud services required.

## Prerequisites
- Python 3.10+
- Node.js 18+ (for the two Next.js apps)

## 1. Clone & configure
```bash
git clone <repo-url> kasamor-platform
cd kasamor-platform
cp .env.example .env   # optional; defaults work out of the box
```

## 2. Ingest the base knowledge package
Place `KASAMOR_Latest_Base_Knowledge_Package_Clean.zip` somewhere and run:
```bash
python3 scripts/ingest_base_knowledge.py --zip /path/to/KASAMOR_Latest_Base_Knowledge_Package_Clean.zip
```
This writes:
- `data/extracted-knowledge/knowledge_chunks.jsonl`
- `data/extracted-knowledge/document_registry.json`
- `data/extracted-knowledge/knowledge_index_summary.md`

## 3. Run the API
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload --port 8000
```
Check: `curl http://localhost:8000/health` and open `http://localhost:8000/docs`.

## 4. Run the mock agent pipeline (no keys needed)
```bash
python3 scripts/run_mock_agent_pipeline.py
# -> data/outputs/reports/KSM-FP-0001_report.md
```

## 5. Run the front-ends
```bash
# Internal console
cd apps/internal-console && npm install && npm run dev   # http://localhost:3001

# Public interface (new terminal)
cd apps/public-interface && npm install && npm run dev    # http://localhost:3000
```
Both apps fall back to bundled mock data if the API is not running.

## Useful scripts
| Script | Purpose |
|---|---|
| `scripts/ingest_base_knowledge.py` | Ingest the ZIP into JSONL chunks. |
| `scripts/create_sample_field_packet.py` | Create another sample packet. |
| `scripts/run_mock_agent_pipeline.py` | Run the full pipeline for one packet. |
| `scripts/export_demo_report.py` | Report for every packet + MVP summary. |

## Troubleshooting
- **Empty knowledge summary** → run the ingestion script (step 2).
- **CORS errors in the browser** → confirm the API is on port 8000; the apps allow
  `localhost:3000` and `localhost:3001` by default.
- **No API running** → front-ends still render using bundled mock data.
