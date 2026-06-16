from __future__ import annotations

from fastapi import APIRouter

from .._loaders import retrieval
from ..schemas.models import (
    KnowledgeChunkResult,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
    KnowledgeSummaryResponse,
)
from .. import storage

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/summary", response_model=KnowledgeSummaryResponse)
def knowledge_summary() -> KnowledgeSummaryResponse:
    registry = storage.load_document_registry()
    chunks = storage.load_chunks()

    domains: dict[str, int] = {}
    sensitivity: dict[str, int] = {}
    for c in chunks:
        domains[c.get("knowledge_domain", "unknown")] = (
            domains.get(c.get("knowledge_domain", "unknown"), 0) + 1
        )
        sensitivity[c.get("sensitivity_level", "INTERNAL")] = (
            sensitivity.get(c.get("sensitivity_level", "INTERNAL"), 0) + 1
        )

    doc_types: dict[str, int] = {}
    doc_count = 0
    if registry:
        doc_count = registry.get("document_count", 0)
        for d in registry.get("documents", []):
            doc_types[d.get("document_type", "unknown")] = (
                doc_types.get(d.get("document_type", "unknown"), 0) + 1
            )

    return KnowledgeSummaryResponse(
        document_count=doc_count,
        chunk_count=len(chunks),
        domains=domains,
        sensitivity_counts=sensitivity,
        document_types=doc_types,
        ingested=bool(chunks),
    )


@router.post("/search", response_model=KnowledgeSearchResponse)
def knowledge_search(req: KnowledgeSearchRequest) -> KnowledgeSearchResponse:
    results = retrieval().search(
        req.query,
        knowledge_domain=req.knowledge_domain,
        max_sensitivity=req.max_sensitivity.value,
        top_k=req.top_k,
    )
    return KnowledgeSearchResponse(
        query=req.query,
        result_count=len(results),
        results=[KnowledgeChunkResult(**r) for r in results],
    )
