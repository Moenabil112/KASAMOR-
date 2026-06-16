#!/usr/bin/env python3
"""
KASAMOR — Lightweight API import/startup validation
===================================================

Verifies the FastAPI app imports cleanly, all route modules are importable, the
expected endpoints are registered, and the OpenAPI schema builds — without
requiring a running server or extra HTTP-client dependencies.

Usage:
    python3 scripts/validate_api.py
Exit 0 if all checks pass, 1 otherwise.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

# Ensure the repo root is importable (so `services` resolves when run as a script).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

EXPECTED_PATHS = {
    "/health",
    "/knowledge/summary",
    "/knowledge/search",
    "/field-packets",
    "/field-packets/{packet_id}",
    "/agents/run/mock",
    "/reports/field-packet/{packet_id}",
}

ROUTE_MODULES = [
    "services.api.routes.health",
    "services.api.routes.knowledge",
    "services.api.routes.field_packets",
    "services.api.routes.agents",
    "services.api.routes.reports",
]


def main() -> int:
    ok = True

    # 1. App imports.
    try:
        from services.api.main import app
        print("[PASS] services.api.main:app imports")
    except Exception as exc:
        print(f"[FAIL] app import: {exc}")
        return 1

    # 2. Route modules import.
    for mod in ROUTE_MODULES:
        try:
            importlib.import_module(mod)
            print(f"[PASS] import {mod}")
        except Exception as exc:
            print(f"[FAIL] import {mod}: {exc}")
            ok = False

    # 3. OpenAPI schema builds (exercises route/model registration) and is the
    #    canonical list of registered endpoints (covers included routers).
    try:
        schema = app.openapi()
        assert schema.get("openapi")
        registered = set(schema.get("paths", {}).keys())
        print(f"[PASS] OpenAPI schema builds ({len(registered)} paths)")
    except Exception as exc:
        print(f"[FAIL] OpenAPI build: {exc}")
        return 1

    # 4. Expected routes are registered.
    missing = EXPECTED_PATHS - registered
    if missing:
        print(f"[FAIL] missing routes: {sorted(missing)}")
        ok = False
    else:
        print(f"[PASS] all {len(EXPECTED_PATHS)} expected routes registered")

    print("=" * 60)
    print("RESULT:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
