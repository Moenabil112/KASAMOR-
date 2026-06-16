"""
KASAMOR Report Generator — Field Packet report (Markdown)
=========================================================

Builds a human-readable Markdown report for a Field Packet from the mock agent
pipeline output. Writes to data/outputs/reports/.

The report is review-oriented: it summarises what data was included, photo/voice
quality, the AI observation summary, and the recommended next action — always
with a sensitivity note and no raw coordinates.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "outputs" / "reports"

SENSITIVITY_NOTE = (
    "This report is INTERNAL. It contains a general place label only — no raw "
    "GPS coordinates and no contributor identity. AI output is assistive and "
    "indicative; it does not confirm the presence or value of any mineral. Final "
    "decisions rest with the House of Earth Trust."
)


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(
    field_packet: dict,
    *,
    photos: list[dict] | None = None,
    voice_notes: list[dict] | None = None,
    pipeline: dict | None = None,
    write: bool = True,
) -> tuple[str, str, Path | None]:
    """Return (markdown, report_id, path). Path is None when write=False."""
    packet_id = field_packet.get("field_packet_id", "KSM-FP-0000")
    report_id = f"KSM-RP-{packet_id.split('-')[-1]}"

    pipeline = pipeline or {}
    observation = pipeline.get("observation", {})
    review = pipeline.get("review", {})
    review_card = pipeline.get("review_card", {})

    # Photo quality summary.
    photo_summary = "No photos attached."
    for step in pipeline.get("steps", []):
        if step.get("agent") == "photo_quality_agent" and step.get("output"):
            photo_summary = step["output"].get("summary", photo_summary)

    # Voice summary.
    voice_summary = "No voice notes attached."
    for step in pipeline.get("steps", []):
        if step.get("agent") == "voice_to_knowledge_agent" and step.get("output"):
            voice_summary = step["output"].get("summary", voice_summary)

    ai_summary = observation.get("summary") or review_card.get("ai_summary") or "Not generated."
    next_action = observation.get("recommended_next_step", "Route to House of Earth Trust review.")
    decision_options = review.get("suggested_decision_options", [])

    data_included = []
    if field_packet.get("photos"):
        data_included.append(f"{len(field_packet['photos'])} photo reference(s)")
    if field_packet.get("voice_notes"):
        data_included.append(f"{len(field_packet['voice_notes'])} voice note(s)")
    if field_packet.get("local_notes"):
        data_included.append(f"{len(field_packet['local_notes'])} local note(s)")
    if field_packet.get("sediment_observations"):
        data_included.append("sediment observations")
    if field_packet.get("rock_observations"):
        data_included.append("rock observations")
    if field_packet.get("water_drainage_observations"):
        data_included.append("water/drainage observations")

    md = f"""# KASAMOR Field Packet Report

**Report ID:** {report_id}
**Field Packet ID:** {packet_id}
**Contributor code:** {field_packet.get('contributor_code', 'n/a')}
**Place label:** {field_packet.get('place_label', 'n/a')}
**Observation date:** {field_packet.get('observation_date', 'n/a')}
**Seasonal context:** {field_packet.get('seasonal_context', 'unknown')}
**Generated:** {_now()}

---

## Data included
{_bullets(data_included) if data_included else '- (none)'}

## Photo quality summary
{photo_summary}

## Voice observation summary
{voice_summary}

## AI observation summary
{ai_summary}

### Indicators (qualitative, not confirmation)
{_indicators(observation.get('indicators', []))}

### AI limitations
{_bullets(observation.get('ai_limitations', ['Mock pipeline output.']))}

## Recommended next action
{next_action}

## Human review
**Current status:** {field_packet.get('review_status', 'pending')}
**Decision options for the House of Earth Trust:**
{_bullets(decision_options) if decision_options else '- (pending pipeline)'}

---

> _Sensitivity note:_ {SENSITIVITY_NOTE}
"""

    path = None
    if write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUT_DIR / f"{packet_id}_report.md"
        path.write_text(md, encoding="utf-8")
    return md, report_id, path


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) if items else "- (none)"


def _indicators(indicators: list[dict]) -> str:
    if not indicators:
        return "- (none detected)"
    return "\n".join(
        f"- **{i.get('name')}** — signal: `{i.get('signal')}` (source: {i.get('source')})"
        for i in indicators
    )


if __name__ == "__main__":
    import json

    fp = json.loads((ROOT / "data" / "field-packets" / "sample_field_packet.json").read_text())
    # Lazy import of the orchestrator to enrich the packet.
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "reg", ROOT / "services" / "agent-orchestrator" / "registry.py"
    )
    reg = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(reg)  # type: ignore[union-attr]
    ph = json.loads((ROOT / "data" / "media" / "sample_photo_metadata.json").read_text())
    vn = json.loads((ROOT / "data" / "media" / "sample_voice_note.json").read_text())
    run = reg.run_pipeline(fp, photos=ph, voice_notes=vn)
    _, rid, p = build_report(fp, photos=ph, voice_notes=vn, pipeline=run, write=True)
    print(f"wrote {p} ({rid})")
