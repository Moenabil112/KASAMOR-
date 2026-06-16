"""
KASAMOR API — FastAPI application
=================================

Local-first MVP API. Reads/writes JSON files under ./data. No database required.

Run:
    uvicorn services.api.main:app --reload --port 8000

Endpoints:
    GET  /health
    GET  /knowledge/summary
    POST /knowledge/search
    GET  /field-packets
    GET  /field-packets/{id}
    POST /field-packets
    POST /agents/run/mock
    POST /reports/field-packet/{id}
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Support both `uvicorn services.api.main:app` (package) and direct execution.
try:
    from .routes import agents, field_packets, health, knowledge, reports
except ImportError:  # pragma: no cover - direct execution fallback
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from services.api.routes import agents, field_packets, health, knowledge, reports

app = FastAPI(
    title="KASAMOR Core API",
    description=(
        "Rural Mineral Intelligence Ecosystem — internal core API. "
        "Local-first MVP with mock AI agents. Sensitive field data is never "
        "exposed through public surfaces."
    ),
    version="0.1.0",
)

# Permit the two local front-ends during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(knowledge.router)
app.include_router(field_packets.router)
app.include_router(agents.router)
app.include_router(reports.router)


@app.get("/", tags=["system"])
def root() -> dict:
    return {
        "name": "KASAMOR Core API",
        "product": "Rural Mineral Intelligence Ecosystem",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": [
            "/health",
            "/knowledge/summary",
            "/knowledge/search",
            "/field-packets",
            "/field-packets/{id}",
            "/agents/run/mock",
            "/reports/field-packet/{id}",
        ],
    }
