"""
KASAMOR Agent Orchestrator — Mock agent implementations
=======================================================

Deterministic implementations of the six MVP agents. Each function honours the
input/output contract described in the matching `agents/*.md` specification, but
returns stable, offline output so the platform runs with NO API keys.

Swap these for live, provider-agnostic model calls in a later sprint
(KASAMOR_AGENT_MODE=live) without changing the orchestrator or API.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

_SERVICES = Path(__file__).resolve().parents[2]


def _load(rel: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, _SERVICES / rel)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


_photo = _load("media-processing/photo_quality.py", "kasamor_photo_quality")
_voice = _load("media-processing/voice_metadata.py", "kasamor_voice_metadata")
try:
    _retrieval = _load("rag-service/retrieval.py", "kasamor_retrieval_orch")
except Exception:  # pragma: no cover
    _retrieval = None


# --------------------------------------------------------------------------- #
# Agent 1 — Knowledge Retrieval
# --------------------------------------------------------------------------- #
def knowledge_retrieval_agent(
    question: str,
    knowledge_domain: str | None = None,
    max_sensitivity: str = "INTERNAL",
) -> dict:
    chunks = (
        _retrieval.search(
            question, knowledge_domain=knowledge_domain, max_sensitivity=max_sensitivity
        )
        if _retrieval
        else []
    )
    if chunks:
        top = chunks[0]
        answer = (
            f"Based on the base knowledge, the most relevant material is from "
            f"\"{top.get('section_title')}\". {top.get('snippet')}"
        )
        confidence = "medium" if len(chunks) >= 2 else "low"
    else:
        answer = "No relevant knowledge was retrieved for this question."
        confidence = "low"
    return {
        "answer": answer,
        "source_chunks": [
            {
                "chunk_id": c["chunk_id"],
                "section_title": c.get("section_title"),
                "score": c.get("score"),
            }
            for c in chunks
        ],
        "confidence": confidence,
        "sensitivity_warning": None,
    }


# --------------------------------------------------------------------------- #
# Agent 2 — Field Packet Intake
# --------------------------------------------------------------------------- #
def field_packet_intake_agent(field_packet: dict) -> dict:
    missing: list[str] = []
    warnings: list[str] = []

    if not field_packet.get("contributor_code"):
        missing.append("contributor_code")
    if not field_packet.get("place_label"):
        missing.append("place_label")
    if not field_packet.get("observation_date"):
        missing.append("observation_date")

    has_evidence = any(
        field_packet.get(k)
        for k in ("photos", "voice_notes", "local_notes")
    )
    if not has_evidence:
        missing.append("evidence (photos / voice_notes / local_notes)")

    season = field_packet.get("seasonal_context", "unknown")
    valid_seasons = {"before_rain", "during_rain", "after_rain", "dry_season", "unknown"}
    normalized_season = season if season in valid_seasons else "unknown"
    if normalized_season != season:
        warnings.append(f"seasonal_context '{season}' normalized to 'unknown'")

    loc = field_packet.get("location") or {}
    if loc and loc.get("sensitivity_level") not in (None, "RESTRICTED"):
        warnings.append(
            "location.sensitivity_level is not RESTRICTED — flag for trust review"
        )

    return {
        "field_packet_id": field_packet.get("field_packet_id"),
        "missing_fields": missing,
        "data_quality_warnings": warnings,
        "normalized_fields": {"seasonal_context": normalized_season},
        "ready_for_review": len(missing) == 0,
    }


# --------------------------------------------------------------------------- #
# Agent 3 — Photo Quality
# --------------------------------------------------------------------------- #
def photo_quality_agent(photos: list[dict]) -> dict:
    return _photo.assess_photos(photos)


# --------------------------------------------------------------------------- #
# Agent 4 — Voice-to-Knowledge
# --------------------------------------------------------------------------- #
def voice_to_knowledge_agent(voice_notes: list[dict]) -> dict:
    return _voice.structure_voice_notes(voice_notes)


# --------------------------------------------------------------------------- #
# Agent 5 — Geo-Photo-Voice Fusion
# --------------------------------------------------------------------------- #
def geo_photo_voice_fusion_agent(
    field_packet: dict,
    photo_results: dict,
    voice_results: dict,
    knowledge_context: dict | None = None,
) -> dict:
    indicators: list[dict] = []

    # Voice-derived indicators.
    for vr in voice_results.get("results", []):
        so = vr.get("structured_observations", {})
        mapping = {
            "seasonal_flow": "seasonal water flow",
            "black_sand_after_flow": "dark/heavy sand after flow",
            "upstream_white_rocks": "upstream quartz-like fragments",
            "persistent_vegetation": "persistent vegetation",
        }
        for key, label in mapping.items():
            signal = "present" if so.get(key) == "reported" else "uncertain"
            indicators.append({"name": label, "signal": signal, "source": "voice"})

    # Photo-derived indicator (documentation quality only).
    counts = photo_results.get("counts", {})
    if counts:
        usable = counts.get("accepted", 0) + counts.get("documentation_only", 0)
        indicators.append(
            {
                "name": "usable supporting photos",
                "signal": "present" if usable else "absent",
                "source": "photo",
            }
        )

    place = field_packet.get("place_label") or "the observation sector"
    summary = (
        f"Field observation at {place}. The contributor reports seasonal drainage "
        "and dark/heavy sand collecting in channel traps after flow, with "
        "quartz-like fragments upstream. Photos provide supporting documentation. "
        "These are qualitative field indicators only — not a confirmation of any "
        "mineral or its value."
    )

    ai_limitations = [
        "Mock analysis: no real image vision or audio transcription was performed.",
        "Indicators describe field context only; they do not confirm mineral presence or value.",
        "Confidence is capped at 'medium' pending House of Earth Trust review.",
    ]

    present_count = sum(1 for i in indicators if i["signal"] == "present")
    confidence = "medium" if present_count >= 2 else "low"

    return {
        "observation_id": f"KSM-OB-{str(field_packet.get('field_packet_id','0001')).split('-')[-1]}",
        "field_packet_id": field_packet.get("field_packet_id"),
        "summary": summary,
        "indicators": indicators,
        "confidence": confidence,
        "recommended_next_step": (
            "Schedule a structured field revisit to re-document the dark sand with a "
            "reference scale and record flow duration after the next rain."
        ),
        "ai_limitations": ai_limitations,
        "needs_human_review": True,
        "sensitivity_level": "INTERNAL",
    }


# --------------------------------------------------------------------------- #
# Agent 6 — House of Earth Trust Review
# --------------------------------------------------------------------------- #
def house_of_earth_trust_review_agent(
    field_packet: dict,
    observation: dict,
    photo_results: dict,
    voice_results: dict,
) -> dict:
    data_included: list[str] = []
    if field_packet.get("photos"):
        data_included.append(f"{len(field_packet['photos'])} photo(s)")
    if field_packet.get("voice_notes"):
        data_included.append(f"{len(field_packet['voice_notes'])} voice note(s)")
    if field_packet.get("local_notes"):
        data_included.append(f"{len(field_packet['local_notes'])} local note(s)")

    review_card = {
        "field_packet_id": field_packet.get("field_packet_id"),
        "place_label": field_packet.get("place_label"),
        "data_summary": (
            "Includes: " + (", ".join(data_included) if data_included else "no media")
            + ". Photo state — " + photo_results.get("summary", "n/a")
            + " Voice state — " + voice_results.get("summary", "n/a")
        ),
        "ai_summary": observation.get("summary"),
        "ai_limitations": observation.get("ai_limitations", []),
        "open_questions": [
            "Is the dark-sand context consistent with the surrounding geology on record?",
            "Does the upstream rock description warrant a sample request?",
            "Is a field revisit justified given current evidence quality?",
        ],
    }
    return {
        "review_card": review_card,
        "suggested_decision_options": [
            "accepted",
            "needs_more_photos",
            "needs_field_revisit",
            "needs_sample",
            "low_priority",
            "rejected",
        ],
    }
