from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import storage
from .._loaders import orchestrator
from ..schemas.models import AgentRunRequest, AgentRunResponse

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/run/mock", response_model=AgentRunResponse)
def run_mock(req: AgentRunRequest) -> AgentRunResponse:
    packet = storage.get_field_packet(req.field_packet_id)
    if not packet:
        raise HTTPException(
            status_code=404, detail=f"Field packet {req.field_packet_id} not found"
        )
    photos = storage.photos_for_packet(req.field_packet_id)
    voices = storage.voice_notes_for_packet(req.field_packet_id)

    result = orchestrator().run_pipeline(
        packet, photos=photos, voice_notes=voices, agents=req.agents
    )
    return AgentRunResponse(
        field_packet_id=req.field_packet_id,
        mode=result["mode"],
        steps=result["steps"],
        review_card=result["review_card"],
    )
