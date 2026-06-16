#!/usr/bin/env python3
"""
KASAMOR — Export demo report(s)
===============================

Runs the mock pipeline for every Field Packet found under data/field-packets/
and exports a Markdown report for each, then writes an MVP build summary.

Output:
    data/outputs/reports/<packet_id>_report.md
    data/outputs/reports/MVP_BUILD_SUMMARY.md
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "data" / "field-packets"
MEDIA = ROOT / "data" / "media"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _all_packets() -> list[dict]:
    out: list[dict] = []
    for p in sorted(PACKETS.glob("*.json")):
        try:
            data = json.loads(p.read_text("utf-8"))
        except json.JSONDecodeError:
            continue
        out.extend(data if isinstance(data, list) else [data])
    return out


def main() -> None:
    registry = _load(ROOT / "services" / "agent-orchestrator" / "registry.py", "reg")
    reporter = _load(
        ROOT / "services" / "report-generator" / "field_packet_report.py", "rep"
    )
    summary = _load(
        ROOT / "services" / "report-generator" / "mvp_summary_report.py", "sum"
    )

    photos = json.loads((MEDIA / "sample_photo_metadata.json").read_text()) if (MEDIA / "sample_photo_metadata.json").exists() else []
    voices = json.loads((MEDIA / "sample_voice_note.json").read_text()) if (MEDIA / "sample_voice_note.json").exists() else []

    count = 0
    for packet in _all_packets():
        pid = packet["field_packet_id"]
        ph = [p for p in photos if p.get("field_packet_id") == pid]
        vn = [v for v in voices if v.get("field_packet_id") == pid]
        run = registry.run_pipeline(packet, photos=ph, voice_notes=vn)
        _, rid, path = reporter.build_report(packet, photos=ph, voice_notes=vn, pipeline=run, write=True)
        print(f"[export] {pid} -> {path}")
        count += 1

    _, sp = summary.build_mvp_summary(write=True)
    print(f"[export] summary -> {sp}")
    print(f"[export] done: {count} report(s).")


if __name__ == "__main__":
    main()
