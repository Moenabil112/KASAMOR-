"""
KASAMOR RAG Service — Local-first retrieval
===========================================

A mock, dependency-free retrieval function over the JSONL knowledge chunks
produced by scripts/ingest_base_knowledge.py.

It performs sensitivity-aware keyword scoring. This is intentionally simple and
deterministic so the MVP runs locally without a vector database or API keys.

Vector backends (pgvector / Qdrant) are reserved for a later sprint; see
`VectorStoreAdapter` for the seam where they plug in.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
CHUNKS_PATH = ROOT / "data" / "extracted-knowledge" / "knowledge_chunks.jsonl"

# Sensitivity ordering: a caller cleared at level N may see chunks at level <= N.
SENSITIVITY_ORDER = {
    "PUBLIC": 0,
    "PARTNER": 1,
    "INTERNAL": 2,
    "RESTRICTED": 3,
    "HOUSE_OF_EARTH_TRUST_ONLY": 4,
}

_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "for", "on",
    "with", "as", "by", "at", "it", "this", "that", "from", "be", "how", "what",
    "who", "does", "do", "can", "kasamor",
}


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z؀-ۿ]+", text.lower()) if t not in _STOPWORDS]


def load_chunks(path: Path = CHUNKS_PATH) -> list[dict]:
    if not path.exists():
        return []
    chunks: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def _visible(chunk: dict, max_level: str) -> bool:
    ceiling = SENSITIVITY_ORDER.get(max_level, 0)
    level = SENSITIVITY_ORDER.get(chunk.get("sensitivity_level", "INTERNAL"), 2)
    return level <= ceiling


def search(
    query: str,
    *,
    knowledge_domain: str | None = None,
    max_sensitivity: str = "INTERNAL",
    top_k: int = 5,
    chunks: Iterable[dict] | None = None,
) -> list[dict]:
    """Return the top_k most relevant, sensitivity-cleared chunks for a query.

    Each result includes a `score` and a `snippet`. Deterministic.
    """
    pool = list(chunks) if chunks is not None else load_chunks()
    q_terms = _tokenize(query)
    q_counts = Counter(q_terms)
    results: list[dict] = []

    for ch in pool:
        if not _visible(ch, max_sensitivity):
            continue
        if knowledge_domain and ch.get("knowledge_domain") != knowledge_domain:
            continue
        body = ch.get("content", "")
        terms = _tokenize(body)
        if not terms:
            continue
        term_counts = Counter(terms)
        # Simple weighted overlap score.
        score = 0.0
        for term, qc in q_counts.items():
            tc = term_counts.get(term, 0)
            if tc:
                score += qc * (1 + math.log(1 + tc))
        # Bonus for section-title matches.
        title = (ch.get("section_title") or "").lower()
        for term in q_counts:
            if term in title:
                score += 1.5
        if score <= 0:
            continue
        results.append(
            {
                "chunk_id": ch["chunk_id"],
                "source_file": ch["source_file"],
                "document_type": ch.get("document_type"),
                "section_title": ch.get("section_title"),
                "knowledge_domain": ch.get("knowledge_domain"),
                "sensitivity_level": ch.get("sensitivity_level"),
                "score": round(score, 3),
                "snippet": _snippet(body, q_terms),
            }
        )

    results.sort(key=lambda r: (-r["score"], r["chunk_id"]))
    return results[:top_k]


def _snippet(body: str, q_terms: list[str], width: int = 240) -> str:
    low = body.lower()
    for term in q_terms:
        idx = low.find(term)
        if idx != -1:
            start = max(0, idx - width // 3)
            end = min(len(body), start + width)
            prefix = "…" if start > 0 else ""
            suffix = "…" if end < len(body) else ""
            return prefix + body[start:end].strip() + suffix
    return body[:width].strip() + ("…" if len(body) > width else "")


class VectorStoreAdapter:
    """Placeholder seam for pgvector / Qdrant backends (later sprint).

    The MVP uses keyword `search()`. A real adapter would implement
    `upsert(chunks)` and `query(embedding, top_k)` and be selected via the
    KASAMOR_VECTOR_BACKEND environment variable.
    """

    backend = "jsonl"

    def query(self, query: str, **kwargs) -> list[dict]:  # pragma: no cover
        return search(query, **kwargs)


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) or "What is the House of Earth Trust?"
    for r in search(q, max_sensitivity="INTERNAL"):
        print(f"[{r['score']:6.2f}] {r['chunk_id']} {r['section_title']}")
        print(f"        {r['snippet'][:120]}")
