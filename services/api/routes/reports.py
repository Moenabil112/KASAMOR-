from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import storage
from .._loaders import orchestrator, report_generator
from ..schemas.models import ReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/field-packet/{packet_id}", response_model=ReportResponse)
def field_packet_report(packet_id: str) -> ReportResponse:
    packet = storage.get_field_packet(packet_id)
    if not packet:
        raise HTTPException(status_code=404, detail=f"Field packet {packet_id} not found")

    photos = storage.photos_for_packet(packet_id)
    voices = storage.voice_notes_for_packet(packet_id)

    # Run the mock pipeline to enrich the packet before reporting.
    run = orchestrator().run_pipeline(packet, photos=photos, voice_notes=voices)
    gen = report_generator()
    markdown, report_id, path = gen.build_report(
        packet, photos=photos, voice_notes=voices, pipeline=run, write=True
    )
    return ReportResponse(
        report_id=report_id,
        field_packet_id=packet_id,
        markdown=markdown,
        path=str(path) if path else None,
    )
