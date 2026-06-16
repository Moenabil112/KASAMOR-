"""
KASAMOR API — Pydantic schemas
==============================

Request/response models for the FastAPI service. These mirror the JSON Schemas
in `/schemas` but are kept lean for the MVP API surface.
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field

from ..models.sensitivity import SensitivityLevel


# --------------------------------------------------------------------------- #
# Knowledge
# --------------------------------------------------------------------------- #
class KnowledgeSearchRequest(BaseModel):
    query: str
    knowledge_domain: Optional[str] = None
    max_sensitivity: SensitivityLevel = SensitivityLevel.INTERNAL
    top_k: int = Field(default=5, ge=1, le=25)


class KnowledgeChunkResult(BaseModel):
    chunk_id: str
    source_file: str
    document_type: Optional[str] = None
    section_title: Optional[str] = None
    knowledge_domain: Optional[str] = None
    sensitivity_level: Optional[str] = None
    score: float
    snippet: str


class KnowledgeSearchResponse(BaseModel):
    query: str
    result_count: int
    results: list[KnowledgeChunkResult]


class KnowledgeSummaryResponse(BaseModel):
    document_count: int
    chunk_count: int
    domains: dict[str, int]
    sensitivity_counts: dict[str, int]
    document_types: dict[str, int]
    ingested: bool


# --------------------------------------------------------------------------- #
# Field Packets
# --------------------------------------------------------------------------- #
class Location(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    accuracy_m: Optional[float] = None
    sensitivity_level: SensitivityLevel = SensitivityLevel.RESTRICTED


class FieldPacket(BaseModel):
    field_packet_id: str
    contributor_code: str
    location: Optional[Location] = None
    place_label: Optional[str] = None
    observation_date: Optional[str] = None
    seasonal_context: str = "unknown"
    photos: list[str] = Field(default_factory=list)
    voice_notes: list[str] = Field(default_factory=list)
    local_notes: list[str] = Field(default_factory=list)
    sediment_observations: list[str] = Field(default_factory=list)
    rock_observations: list[str] = Field(default_factory=list)
    water_drainage_observations: list[str] = Field(default_factory=list)
    observation_tags: list[str] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    review_status: str = "pending"
    review_decision: Optional[str] = None
    created_at: Optional[str] = None


class FieldPacketCreate(BaseModel):
    contributor_code: str
    place_label: Optional[str] = None
    observation_date: Optional[str] = None
    seasonal_context: str = "unknown"
    location: Optional[Location] = None
    local_notes: list[str] = Field(default_factory=list)
    observation_tags: list[str] = Field(default_factory=list)


class FieldPacketSummary(BaseModel):
    field_packet_id: str
    contributor_code: str
    place_label: Optional[str] = None
    review_status: str
    review_decision: Optional[str] = None
    observation_date: Optional[str] = None


# --------------------------------------------------------------------------- #
# Agents & reports
# --------------------------------------------------------------------------- #
class AgentRunRequest(BaseModel):
    field_packet_id: str
    agents: Optional[list[str]] = None  # default: full pipeline


class AgentRunResponse(BaseModel):
    field_packet_id: str
    mode: str
    steps: list[dict[str, Any]]
    review_card: dict[str, Any]


class ReportResponse(BaseModel):
    report_id: str
    field_packet_id: str
    markdown: str
    path: Optional[str] = None
