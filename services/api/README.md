# KASAMOR Core API (FastAPI)

Local-first MVP API. Reads/writes JSON files under `./data`. **No database required.**

## Run
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r services/api/requirements.txt
uvicorn services.api.main:app --reload --port 8000
```
Interactive docs at `http://localhost:8000/docs`.

## Endpoints
| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/knowledge/summary` | Document/chunk/domain/sensitivity counts |
| POST | `/knowledge/search` | Sensitivity-aware mock retrieval |
| GET | `/field-packets` | List sample/created packets |
| GET | `/field-packets/{id}` | Packet detail |
| POST | `/field-packets` | Create a packet (local JSON) |
| POST | `/agents/run/mock` | Run the mock agent pipeline for a packet |
| POST | `/reports/field-packet/{id}` | Generate + export a Markdown report |

## Notes
- Sensitivity is enforced by `models/sensitivity.py`. Raw coordinates and
  contributor codes are never returned through public surfaces.
- AI agents run as deterministic **mocks** (`KASAMOR_AGENT_MODE=mock`). Provider
  wiring is a later sprint.
- Storage lives in `storage.py`; swap it for PostgreSQL/PostGIS later without
  touching the route handlers.
