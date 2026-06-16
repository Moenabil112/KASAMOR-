"""
KASAMOR RAG Service — Ingestion entrypoint (thin wrapper)
=========================================================

The authoritative ingestion pipeline lives in
`scripts/ingest_base_knowledge.py` so it can run with zero dependencies from a
clean checkout. This module exposes it as an importable function for services
and tests.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "ingest_base_knowledge.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("kasamor_ingest", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def run_ingestion(zip_path: str | None = None) -> dict:
    """Run base-knowledge ingestion and return a small summary dict."""
    mod = _load_script_module()
    base = mod.discover_package(zip_path)
    chunks, registry = mod.ingest(base)
    mod.write_outputs(chunks, registry)
    return {"documents": len(registry), "chunks": len(chunks)}


if __name__ == "__main__":
    import sys

    zip_arg = sys.argv[1] if len(sys.argv) > 1 else None
    print(run_ingestion(zip_arg))
