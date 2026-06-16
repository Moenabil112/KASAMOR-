"""
KASAMOR Media Processing — Photo Quality (mock)
===============================================

Deterministic, dependency-free photo-quality assessment for the MVP. Inspects
photo metadata (and filename hints) and returns a quality verdict + simple
field-facing feedback.

IMPORTANT: This module NEVER identifies minerals and NEVER asserts value from an
image. It assesses suitability for analysis vs documentation only.
"""
from __future__ import annotations

CLOSEUP_TYPES = {
    "sediment_closeup",
    "black_sand_closeup",
    "trap_closeup",
    "quartz_fragment",
    "magnet_test",
    "sample_id",
}


def assess_photo(meta: dict) -> dict:
    """Return a quality result for a single photo metadata dict."""
    notes: list[str] = list(meta.get("quality_notes") or [])
    photo_type = meta.get("photo_type", "other")
    is_blurry = bool(meta.get("is_blurry"))
    has_scale = bool(meta.get("has_reference_scale"))
    lighting = meta.get("lighting_condition", "unknown")

    status = "accepted"
    feedback = "Looks good for documentation."

    if is_blurry:
        status = "needs_retake"
        feedback = "Photo is blurry — please retake holding the phone steady."
        notes.append("blurry")
    elif photo_type in CLOSEUP_TYPES and not has_scale:
        status = "needs_retake"
        feedback = "Close-up needs a reference scale (e.g. a coin) in the frame."
        notes.append("no_reference_scale")
    elif lighting == "poor":
        status = "documentation_only"
        feedback = "Usable for documentation; lighting is poor for detail."
        notes.append("poor_lighting")
    elif lighting == "unknown" and photo_type in CLOSEUP_TYPES:
        status = "documentation_only"
        feedback = "Kept for documentation; not reliable for measurement."

    return {
        "photo_id": meta.get("photo_id"),
        "field_packet_id": meta.get("field_packet_id"),
        "photo_type": photo_type,
        "quality_status": status,
        "field_feedback": feedback,
        "quality_notes": notes,
        "has_reference_scale": has_scale,
        "is_blurry": is_blurry,
        "lighting_condition": lighting,
        # No mineral identification is ever produced here.
        "ai_confidence": meta.get("ai_confidence", "low"),
    }


def assess_photos(photos: list[dict]) -> dict:
    """Assess a list of photos; return per-photo results + a short summary."""
    results = [assess_photo(p) for p in photos]
    counts: dict[str, int] = {}
    for r in results:
        counts[r["quality_status"]] = counts.get(r["quality_status"], 0) + 1
    if not results:
        summary = "No photos attached to this packet."
    else:
        parts = [f"{n}× {s}" for s, n in sorted(counts.items())]
        summary = f"{len(results)} photo(s): " + ", ".join(parts) + "."
    return {"results": results, "summary": summary, "counts": counts}


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path

    sample = Path(__file__).resolve().parents[2] / "data" / "media" / "sample_photo_metadata.json"
    photos = json.loads(sample.read_text("utf-8")) if sample.exists() else []
    print(json.dumps(assess_photos(photos), indent=2, ensure_ascii=False))
