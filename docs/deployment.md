# KASAMOR — Deployment Notes

The MVP targets **local-first** operation. This document outlines how the pieces
would be deployed beyond a laptop, and what is intentionally deferred.

## Topology

```
[ public-interface ]   [ internal-console ]
        │                      │
        └──────── NEXT_PUBLIC_API_BASE_URL ───────┐
                                                   ▼
                                           [ services/api ]
                                                   │
                                      local JSON (MVP) / Postgres (later)
```

## Option A — Docker Compose (convenience)
A `docker-compose.yml` is provided. The first demo does **not** require it.
```bash
docker compose up api                # API on :8000
docker compose up public-interface   # :3000
docker compose up internal-console   # :3001
```
The `db` (PostGIS) service is commented out — the MVP uses local JSON.

## Option B — Manual
- **API**: any host with Python 3.10+. `uvicorn services.api.main:app`.
- **Front-ends**: `npm run build && npm run start` per app, or deploy to a static/
  edge host (e.g. Vercel). Set `NEXT_PUBLIC_API_BASE_URL` to the API URL.

## Environment
See `.env.example`. The MVP runs with all values at their defaults. Notable knobs:
- `KASAMOR_AGENT_MODE` — `mock` (default) or `live` (future).
- `KASAMOR_VECTOR_BACKEND` — `jsonl` (default), `pgvector`/`qdrant` (future).

## Security & governance for production (later sprint)
- Add authentication + role-based access (contributor / reviewer / trust / partner).
- Keep RESTRICTED and HOUSE_OF_EARTH_TRUST_ONLY data off any public network path.
- Terminate TLS; restrict CORS to known origins.
- Never deploy the public interface with anything above PUBLIC sensitivity.

## Deferred infrastructure
- PostgreSQL/PostGIS for packets, media, and geospatial queries.
- Vector store (pgvector/Qdrant) for semantic retrieval.
- Object storage for raw media with signed, access-controlled URLs.
- Real, provider-agnostic AI model wiring.
