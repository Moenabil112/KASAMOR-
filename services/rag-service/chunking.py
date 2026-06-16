"""
KASAMOR RAG Service — Chunking utilities
========================================

Shared chunking helpers. The ingestion script (scripts/ingest_base_knowledge.py)
contains the authoritative pipeline; these helpers are re-exported here so other
services and a future re-chunking job can reuse them without duplicating logic.
"""
from __future__ import annotations

import re

SECTION_RE = re.compile(
    r"^\s*(?:SECTION\s+\d+|[0-9]+(?:\.[0-9]+)*\s+\S|#{1,6}\s+\S).*$",
    re.IGNORECASE,
)


def split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split document text into (section_title, body) pairs by headings."""
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    body: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if SECTION_RE.match(line) and len(line) < 120:
            if body:
                sections.append((current_title, "\n".join(body).strip()))
                body = []
            current_title = re.sub(r"^#{1,6}\s+", "", line).strip()
        else:
            body.append(line)
    if body:
        sections.append((current_title, "\n".join(body).strip()))
    return sections or [("Overview", text.strip())]


def chunk_section(body: str, max_chars: int = 1400) -> list[str]:
    """Break a long section body into paragraph-aware chunks."""
    if len(body) <= max_chars:
        return [body] if body.strip() else []
    chunks: list[str] = []
    buf: list[str] = []
    size = 0
    for para in body.split("\n"):
        p = para.strip()
        if not p:
            continue
        if size + len(p) > max_chars and buf:
            chunks.append("\n".join(buf).strip())
            buf, size = [], 0
        buf.append(p)
        size += len(p) + 1
    if buf:
        chunks.append("\n".join(buf).strip())
    return [c for c in chunks if c.strip()]


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
