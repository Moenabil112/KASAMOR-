from __future__ import annotations

import datetime as _dt

from fastapi import APIRouter, HTTPException

from .. import storage
from ..schemas.models import (
    FieldPacket,
    FieldPacketCreate,
    FieldPacketSummary,
)

router = APIRouter(prefix="/field-packets", tags=["field-packets"])


@router.get("", response_model=list[FieldPacketSummary])
def list_packets() -> list[FieldPacketSummary]:
    out: list[FieldPacketSummary] = []
    for pk in storage.list_field_packets():
        out.append(
            FieldPacketSummary(
                field_packet_id=pk["field_packet_id"],
                contributor_code=pk.get("contributor_code", "unknown"),
                place_label=pk.get("place_label"),
                review_status=pk.get("review_status", "pending"),
                review_decision=pk.get("review_decision"),
                observation_date=pk.get("observation_date"),
            )
        )
    return out


@router.get("/{packet_id}", response_model=FieldPacket)
def get_packet(packet_id: str) -> FieldPacket:
    pk = storage.get_field_packet(packet_id)
    if not pk:
        raise HTTPException(status_code=404, detail=f"Field packet {packet_id} not found")
    return FieldPacket(**pk)


@router.post("", response_model=FieldPacket, status_code=201)
def create_packet(body: FieldPacketCreate) -> FieldPacket:
    packet_id = storage.next_field_packet_id()
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    packet = {
        "field_packet_id": packet_id,
        "contributor_code": body.contributor_code,
        "location": (body.location.model_dump() if body.location else None),
        "place_label": body.place_label,
        "observation_date": body.observation_date,
        "seasonal_context": body.seasonal_context,
        "photos": [],
        "voice_notes": [],
        "local_notes": body.local_notes,
        "sediment_observations": [],
        "rock_observations": [],
        "water_drainage_observations": [],
        "observation_tags": body.observation_tags,
        "ai_summary": None,
        "review_status": "pending",
        "review_decision": None,
        "created_at": now,
    }
    storage.save_field_packet(packet)
    return FieldPacket(**packet)
