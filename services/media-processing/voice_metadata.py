"""
KASAMOR Media Processing — Voice-to-Knowledge (mock)
====================================================

Deterministic, dependency-free voice-note structuring for the MVP. In mock mode
it produces a representative transcript and maps simple keyword cues to the
structured observation fields. It does NOT call a real transcription model.

IMPORTANT: This module preserves what a contributor reported. It never upgrades
local belief into geological fact and never asserts mineral value.
"""
from __future__ import annotations

# A representative mock transcript used when no real transcript is present. It
# reflects the kind of seasonal field observation the system is designed for.
_MOCK_TRANSCRIPT = (
    "After the heavy rain the channel runs for two or three days, then it dries. "
    "When the water slows at the bend, a dark heavy sand stays behind in the "
    "traps. Up the slope there are white rock pieces. The green bushes here stay "
    "longer than in the open ground. I am fairly sure about the dark sand."
)

_KEYWORDS = {
    "seasonal_flow": ["rain", "runs", "flow", "water", "dries", "channel"],
    "black_sand_after_flow": ["dark", "black", "heavy sand", "traps", "dark sand"],
    "upstream_white_rocks": ["white rock", "white rocks", "quartz", "up the slope"],
    "persistent_vegetation": ["green", "bushes", "vegetation", "stay longer"],
}


def _detect(text: str, terms: list[str]) -> str | None:
    low = text.lower()
    hits = [t for t in terms if t in low]
    return "reported" if hits else None


def structure_voice_note(note: dict) -> dict:
    """Return a structured result for one voice note (mock)."""
    transcript = note.get("transcript") or _MOCK_TRANSCRIPT
    structured = {
        "seasonal_flow": _detect(transcript, _KEYWORDS["seasonal_flow"]),
        "black_sand_after_flow": _detect(transcript, _KEYWORDS["black_sand_after_flow"]),
        "upstream_white_rocks": _detect(transcript, _KEYWORDS["upstream_white_rocks"]),
        "persistent_vegetation": _detect(transcript, _KEYWORDS["persistent_vegetation"]),
        "local_confidence": "medium" if "sure" in transcript.lower() else "unknown",
    }
    detected = sum(1 for v in structured.values() if v == "reported")
    confidence = "medium" if detected >= 2 else "low"

    follow_up = (
        "Next time, can you record roughly how many days the water flows after "
        "rain, and point the camera at the dark sand with a coin for scale?"
    )

    return {
        "voice_note_id": note.get("voice_note_id"),
        "field_packet_id": note.get("field_packet_id"),
        "language_or_dialect": note.get("language_or_dialect", "unknown"),
        "transcript": transcript,
        "structured_observations": structured,
        "confidence": confidence,
        "follow_up_question": follow_up,
    }


def structure_voice_notes(notes: list[dict]) -> dict:
    results = [structure_voice_note(n) for n in notes]
    if not results:
        summary = "No voice notes attached to this packet."
    else:
        reported = []
        for r in results:
            for k, v in r["structured_observations"].items():
                if v == "reported":
                    reported.append(k)
        uniq = sorted(set(reported))
        summary = (
            f"{len(results)} voice note(s). Reported field cues: "
            + (", ".join(uniq) if uniq else "none clearly detected")
            + "."
        )
    return {"results": results, "summary": summary}


if __name__ == "__main__":
    import json
    from pathlib import Path

    sample = Path(__file__).resolve().parents[2] / "data" / "media" / "sample_voice_note.json"
    notes = json.loads(sample.read_text("utf-8")) if sample.exists() else []
    print(json.dumps(structure_voice_notes(notes), indent=2, ensure_ascii=False))
