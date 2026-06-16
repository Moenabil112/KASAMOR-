"""
KASAMOR Agent Orchestrator — Registry & pipeline
================================================

Maps the six agent ids to callable implementations and runs the standard MVP
pipeline. Provider-agnostic: the registry selects a backend based on
KASAMOR_AGENT_MODE (default "mock"). Only "mock" is implemented in the MVP; a
"live" backend would register the same ids with real model calls.
"""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

_HERE = Path(__file__).resolve().parent


def _load(rel: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, _HERE / rel)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


_mock = _load("agents/mock_agents.py", "kasamor_mock_agents")


# Agent id -> callable. Stable contract regardless of backend.
MOCK_REGISTRY = {
    "knowledge_retrieval_agent": _mock.knowledge_retrieval_agent,
    "field_packet_intake_agent": _mock.field_packet_intake_agent,
    "photo_quality_agent": _mock.photo_quality_agent,
    "voice_to_knowledge_agent": _mock.voice_to_knowledge_agent,
    "geo_photo_voice_fusion_agent": _mock.geo_photo_voice_fusion_agent,
    "house_of_earth_trust_review_agent": _mock.house_of_earth_trust_review_agent,
}

DEFAULT_PIPELINE = [
    "field_packet_intake_agent",
    "photo_quality_agent",
    "voice_to_knowledge_agent",
    "geo_photo_voice_fusion_agent",
    "house_of_earth_trust_review_agent",
]


def get_registry(mode: str | None = None) -> dict:
    mode = mode or os.environ.get("KASAMOR_AGENT_MODE", "mock")
    if mode == "mock":
        return MOCK_REGISTRY
    # A "live" backend would be wired here in a later sprint.
    raise NotImplementedError(
        f"Agent mode '{mode}' is not implemented in the MVP. Use KASAMOR_AGENT_MODE=mock."
    )


def run_pipeline(
    field_packet: dict,
    *,
    photos: list[dict] | None = None,
    voice_notes: list[dict] | None = None,
    agents: list[str] | None = None,
    mode: str | None = None,
) -> dict:
    """Run the standard MVP pipeline and return steps + the trust review card."""
    photos = photos or []
    voice_notes = voice_notes or []
    registry = get_registry(mode)
    selected = agents or DEFAULT_PIPELINE

    steps: list[dict] = []
    intake = photo_res = voice_res = observation = review = None

    for agent_id in selected:
        fn = registry.get(agent_id)
        if not fn:
            steps.append({"agent": agent_id, "status": "skipped", "reason": "not registered"})
            continue

        if agent_id == "field_packet_intake_agent":
            output = fn(field_packet)
            intake = output
        elif agent_id == "photo_quality_agent":
            output = fn(photos)
            photo_res = output
        elif agent_id == "voice_to_knowledge_agent":
            output = fn(voice_notes)
            voice_res = output
        elif agent_id == "geo_photo_voice_fusion_agent":
            output = fn(field_packet, photo_res or {}, voice_res or {})
            observation = output
        elif agent_id == "house_of_earth_trust_review_agent":
            output = fn(field_packet, observation or {}, photo_res or {}, voice_res or {})
            review = output
        else:
            output = {"note": "agent has no pipeline binding"}

        steps.append({"agent": agent_id, "status": "ok", "output": output})

    review_card = (review or {}).get("review_card", {})
    # Attach the AI observation summary back onto the packet for reporting.
    if observation:
        review_card.setdefault("ai_summary", observation.get("summary"))

    return {
        "mode": mode or os.environ.get("KASAMOR_AGENT_MODE", "mock"),
        "steps": steps,
        "observation": observation or {},
        "review": review or {},
        "review_card": review_card,
    }


if __name__ == "__main__":
    import json

    root = _HERE.parents[1]
    fp = json.loads((root / "data" / "field-packets" / "sample_field_packet.json").read_text())
    ph = json.loads((root / "data" / "media" / "sample_photo_metadata.json").read_text())
    vn = json.loads((root / "data" / "media" / "sample_voice_note.json").read_text())
    out = run_pipeline(fp, photos=ph, voice_notes=vn)
    print(json.dumps({"steps": [s["agent"] for s in out["steps"]], "review_card": out["review_card"]}, indent=2, ensure_ascii=False))
