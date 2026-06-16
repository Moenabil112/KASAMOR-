"""
Module loaders
==============

Some service directories use hyphens (rag-service, agent-orchestrator,
media-processing, report-generator) and are not importable as normal packages.
These helpers load them by file path so the API can call into them.
"""
from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path
from types import ModuleType

SERVICES = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:  # pragma: no cover
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def retrieval() -> ModuleType:
    return _load(SERVICES / "rag-service" / "retrieval.py", "kasamor_retrieval")


@lru_cache(maxsize=None)
def orchestrator() -> ModuleType:
    return _load(
        SERVICES / "agent-orchestrator" / "registry.py", "kasamor_orchestrator"
    )


@lru_cache(maxsize=None)
def report_generator() -> ModuleType:
    return _load(
        SERVICES / "report-generator" / "field_packet_report.py",
        "kasamor_report_generator",
    )
