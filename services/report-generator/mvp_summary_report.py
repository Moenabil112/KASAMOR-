"""
KASAMOR Report Generator — MVP summary report (Markdown)
========================================================

Produces a one-page build/status summary of the MVP: knowledge ingestion stats,
field packet counts, and a list of generated reports. Useful for demos and as a
Phase-7 artifact.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXTRACTED = ROOT / "data" / "extracted-knowledge"
PACKETS = ROOT / "data" / "field-packets"
REPORTS = ROOT / "data" / "outputs" / "reports"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_mvp_summary(write: bool = True) -> tuple[str, Path | None]:
    registry = {}
    reg_path = EXTRACTED / "document_registry.json"
    if reg_path.exists():
        registry = json.loads(reg_path.read_text("utf-8"))

    packet_files = list(PACKETS.glob("*.json")) if PACKETS.exists() else []
    report_files = list(REPORTS.glob("*_report.md")) if REPORTS.exists() else []

    md = f"""# KASAMOR MVP — Build Summary

**Generated:** {_now()}

## Knowledge base
- Documents ingested: **{registry.get('document_count', 0)}**
- Knowledge chunks: **{registry.get('chunk_count', 0)}**

## Field packets
- Field packet files: **{len(packet_files)}**
{chr(10).join(f'  - {p.name}' for p in sorted(packet_files)) or '  - (none)'}

## Generated reports
{chr(10).join(f'- {r.name}' for r in sorted(report_files)) or '- (none yet — run the mock pipeline)'}

## Status
- API: FastAPI, local JSON storage, mock agents (no API keys required).
- Agents: 6 specifications + deterministic mock execution.
- Front-ends: public interface + internal console (Next.js).

> This is an MVP foundation. Live AI models, vector search, and a database are
> intentionally deferred — see ROADMAP.md.
"""
    path = None
    if write:
        REPORTS.mkdir(parents=True, exist_ok=True)
        path = REPORTS / "MVP_BUILD_SUMMARY.md"
        path.write_text(md, encoding="utf-8")
    return md, path


if __name__ == "__main__":
    _, p = build_mvp_summary(write=True)
    print(f"wrote {p}")
