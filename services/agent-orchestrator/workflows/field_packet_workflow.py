"""
KASAMOR Agent Orchestrator — Field Packet workflow
==================================================

Declarative description of the standard Field Packet workflow. The executable
logic lives in `registry.run_pipeline`; this module documents the ordered stages
and the data each stage consumes/produces, so the workflow can be visualised or
re-ordered without touching execution code.
"""
from __future__ import annotations

FIELD_PACKET_WORKFLOW = [
    {
        "stage": 1,
        "agent": "field_packet_intake_agent",
        "consumes": ["field_packet"],
        "produces": ["missing_fields", "data_quality_warnings", "ready_for_review"],
    },
    {
        "stage": 2,
        "agent": "photo_quality_agent",
        "consumes": ["photos"],
        "produces": ["photo_quality_results", "photo_summary"],
    },
    {
        "stage": 3,
        "agent": "voice_to_knowledge_agent",
        "consumes": ["voice_notes"],
        "produces": ["transcript", "structured_observations", "follow_up_question"],
    },
    {
        "stage": 4,
        "agent": "geo_photo_voice_fusion_agent",
        "consumes": ["field_packet", "photo_quality_results", "structured_observations"],
        "produces": ["observation_summary", "indicators", "confidence"],
    },
    {
        "stage": 5,
        "agent": "house_of_earth_trust_review_agent",
        "consumes": ["field_packet", "observation_summary"],
        "produces": ["review_card", "suggested_decision_options"],
    },
]
