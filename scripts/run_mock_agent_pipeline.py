#!/usr/bin/env python3
"""
KASAMOR — Mock Agent Pipeline (end-to-end demo)
===============================================

Runs the full MVP agent pipeline on the sample Field Packet using deterministic
mock agents (NO API keys required), then exports a Markdown report.

Steps:
    1. Load sample Field Packet (+ photo & voice metadata).
    2. Field Packet Intake Agent (mock).
    3. Photo Quality Agent (mock).
    4. Voice-to-Knowledge Agent (mock).
    5. Geo-Photo-Voice Fusion Agent (mock).
    6. House of Earth Trust Review card.
    7. Export Markdown report.

Output:
    data/outputs/reports/KSM-FP-0001_report.md
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the KASAMOR mock agent pipeline.")
    parser.add_argument(
        "--packet",
        default=str(ROOT / "data" / "field-packets" / "sample_field_packet.json"),
        help="Path to a Field Packet JSON file.",
    )
    args = parser.parse_args()

    registry = _load(ROOT / "services" / "agent-orchestrator" / "registry.py", "reg")
    reporter = _load(
        ROOT / "services" / "report-generator" / "field_packet_report.py", "rep"
    )

    packet = json.loads(Path(args.packet).read_text("utf-8"))
    packet_id = packet["field_packet_id"]

    media_dir = ROOT / "data" / "media"
    photos = [
        p
        for p in _safe_json(media_dir / "sample_photo_metadata.json", [])
        if p.get("field_packet_id") == packet_id
    ]
    voices = [
        v
        for v in _safe_json(media_dir / "sample_voice_note.json", [])
        if v.get("field_packet_id") == packet_id
    ]

    print(f"[pipeline] Field Packet: {packet_id} — {packet.get('place_label')}")
    print(f"[pipeline] photos={len(photos)} voice_notes={len(voices)}\n")

    run = registry.run_pipeline(packet, photos=photos, voice_notes=voices)

    for step in run["steps"]:
        status = step.get("status")
        print(f"[pipeline] {step['agent']:38s} -> {status}")

    print("\n[pipeline] Review card:")
    print(json.dumps(run["review_card"], indent=2, ensure_ascii=False))

    md, report_id, path = reporter.build_report(
        packet, photos=photos, voice_notes=voices, pipeline=run, write=True
    )
    print(f"\n[pipeline] Report {report_id} written to: {path}")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text("utf-8"))
    except json.JSONDecodeError:
        return default


if __name__ == "__main__":
    main()
