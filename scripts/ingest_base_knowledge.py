#!/usr/bin/env python3
"""
KASAMOR — Base Knowledge Ingestion
==================================

Ingest the latest clean base knowledge package and turn it into RAG-ready,
sensitivity-tagged knowledge chunks.

Usage:
    python3 scripts/ingest_base_knowledge.py \
        --zip /path/to/KASAMOR_Latest_Base_Knowledge_Package_Clean.zip

If --zip is omitted, the script looks for an already-extracted package in
data/base-knowledge/.

Outputs:
    data/extracted-knowledge/knowledge_chunks.jsonl
    data/extracted-knowledge/document_registry.json
    data/extracted-knowledge/knowledge_index_summary.md

This script has NO third-party dependencies — DOCX text is read directly from
the underlying Open XML zip so it runs in any plain Python 3 environment.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Iterable

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]
BASE_KNOWLEDGE_DIR = ROOT / "data" / "base-knowledge"
EXTRACTED_DIR = ROOT / "data" / "extracted-knowledge"
GEO_DIR = ROOT / "data" / "geo"

# --------------------------------------------------------------------------- #
# Document classification (filename -> (document_type, knowledge_domain,
# default sensitivity)). Mirrors the MANIFEST of the clean package.
# --------------------------------------------------------------------------- #
DOC_PROFILES: dict[str, tuple[str, str, str]] = {
    "01_kasamor_master_concept": ("master_concept", "concept", "PARTNER"),
    "02_kasamor_academic_blueprint": ("academic_blueprint", "academic", "INTERNAL"),
    "03_kasamor_field_intelligence": ("field_protocol", "field", "INTERNAL"),
    "04_kasamor_mvp_study_area": ("mvp_spotlight", "economic", "PARTNER"),
    "05_kasamor_technical_ai_agent": ("technical_blueprint", "technical", "INTERNAL"),
    "06_kasamor_90-day_mvp": ("mvp_roadmap", "concept", "INTERNAL"),
    "07_kasamor_data_governance": ("governance", "governance", "INTERNAL"),
    "08_kasamor_house_of_earth_trust": ("trust_operating_model", "governance", "INTERNAL"),
    "09_kasamor_rural_training": ("training_manual", "field", "PARTNER"),
    "10_kasamor_field_packet": ("field_templates", "field", "INTERNAL"),
    "11_kasamor_economic": ("economic_model", "economic", "PARTNER"),
    "12_kasamor_risk": ("risk_framework", "risk", "INTERNAL"),
    "13_kasamor_investor": ("partner_brief", "partner", "PARTNER"),
}

DEFAULT_PROFILE = ("supporting_document", "concept", "INTERNAL")

# Section heading detector for DOCX/MD text.
SECTION_RE = re.compile(
    r"^\s*(?:SECTION\s+\d+|[0-9]+(?:\.[0-9]+)*\s+\S|#{1,6}\s+\S).*$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _profile_for(filename: str) -> tuple[str, str, str]:
    key = filename.lower()
    for prefix, profile in DOC_PROFILES.items():
        if prefix in key:
            return profile
    return DEFAULT_PROFILE


def _estimate_tokens(text: str) -> int:
    # Rough heuristic; good enough for an MVP index.
    return max(1, len(text) // 4)


# --------------------------------------------------------------------------- #
# Coordinate redaction
#
# Raw latitude/longitude values, GeoJSON coordinate arrays, KML coordinate
# strings, and exact AOI center references must never reach PUBLIC / PARTNER /
# INTERNAL knowledge chunks. This utility detects such content, replaces it with
# a safe placeholder, and signals that the owning chunk must be sensitivity-
# elevated to RESTRICTED (or HOUSE_OF_EARTH_TRUST_ONLY for private expert/evidence
# context).
# --------------------------------------------------------------------------- #
RESTRICTED_COORDINATE = "[RESTRICTED_COORDINATE]"
PROTECTED_GEOSPATIAL_REFERENCE = "[PROTECTED_GEOSPATIAL_REFERENCE]"

# High-precision decimal that looks like a coordinate component (4+ decimals).
_DEC = r"-?\d{1,3}\.\d{4,}"

_GEOJSON_COORDS = re.compile(r'"coordinates"\s*:\s*\[[\s\S]*?\]', re.IGNORECASE)
_KML_COORDS = re.compile(r"<coordinates>[\s\S]*?</coordinates>", re.IGNORECASE)
_LOOKAT = re.compile(
    r"(lookat_(?:longitude|latitude|altitude|range|heading|tilt))\s*[:=]?\s*-?\d+\.\d+",
    re.IGNORECASE,
)
_JSON_LATLON = re.compile(
    r'"(lat|lon|latitude|longitude|center_longitude|center_latitude)"\s*:\s*-?\d+\.\d+',
    re.IGNORECASE,
)
_PROSE_PAIR = re.compile(rf"{_DEC}\s*,\s*{_DEC}")
_LATLON_WORDS = re.compile(rf"(lat(?:itude)?|lon(?:gitude)?)\s+({_DEC})", re.IGNORECASE)
_BARE_HIGHPREC = re.compile(_DEC)

# Coordinate context cue — only then do we redact remaining bare high-precision
# decimals, to avoid touching unrelated numeric figures.
_COORD_CONTEXT = re.compile(
    r"coordinate|latitude|longitude|\baoi\b|geojson|\bkml\b|\bcenter\b|\blat\b|\blon\b|crs84",
    re.IGNORECASE,
)

# Private expert / evidence context -> HOUSE_OF_EARTH_TRUST_ONLY rather than RESTRICTED.
_EXPERT_CONTEXT = re.compile(
    r"private research|evidence register|protected research|expert evidence|geological memory",
    re.IGNORECASE,
)


def redact_coordinates(text: str) -> tuple[str, int, bool]:
    """Redact coordinate-like content from `text`.

    Returns (redacted_text, redaction_count, used_protected_geospatial).
    """
    count = 0
    protected_geo = False

    def _sub(pattern: re.Pattern, repl, s: str) -> str:
        nonlocal count
        new, n = pattern.subn(repl, s)
        count += n
        return new

    out = text

    # Structural geospatial -> PROTECTED_GEOSPATIAL_REFERENCE.
    if _GEOJSON_COORDS.search(out) or _KML_COORDS.search(out):
        protected_geo = True
    out = _sub(_GEOJSON_COORDS, f'"coordinates": {PROTECTED_GEOSPATIAL_REFERENCE}', out)
    out = _sub(_KML_COORDS, f"<coordinates>{PROTECTED_GEOSPATIAL_REFERENCE}</coordinates>", out)
    out = _sub(_LOOKAT, lambda m: f"{m.group(1)}: {PROTECTED_GEOSPATIAL_REFERENCE}", out)

    # JSON lat/lon fields and prose pairs -> RESTRICTED_COORDINATE.
    out = _sub(_JSON_LATLON, lambda m: f'"{m.group(1)}": {RESTRICTED_COORDINATE}', out)
    out = _sub(_PROSE_PAIR, RESTRICTED_COORDINATE, out)
    out = _sub(_LATLON_WORDS, lambda m: f"{m.group(1)} {RESTRICTED_COORDINATE}", out)

    # Remaining bare high-precision decimals, only in clear coordinate context.
    if _COORD_CONTEXT.search(text):
        out = _sub(_BARE_HIGHPREC, RESTRICTED_COORDINATE, out)

    return out, count, protected_geo


def elevated_level_for(text: str, document_type: str) -> str:
    """Sensitivity level a coordinate-bearing chunk must be elevated to."""
    if document_type == "trust_operating_model" or _EXPERT_CONTEXT.search(text):
        return "HOUSE_OF_EARTH_TRUST_ONLY"
    return "RESTRICTED"


def extract_docx_text(path: Path) -> str:
    """Read paragraph text from a .docx without third-party libraries."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
    except Exception as exc:  # pragma: no cover - defensive
        return f"[Could not read {path.name}: {exc}]"
    # Paragraph boundaries -> newlines; tabs -> spaces; strip tags.
    xml = xml.replace("</w:p>", "\n")
    xml = xml.replace("<w:tab/>", "\t")
    xml = re.sub(r"<[^>]+>", "", xml)
    xml = (
        xml.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    # Collapse excessive blank lines.
    lines = [ln.rstrip() for ln in xml.splitlines()]
    return "\n".join(lines)


def split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split document text into (section_title, body) pairs by headings."""
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_body: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if SECTION_RE.match(line) and len(line) < 120:
            if current_body:
                sections.append((current_title, "\n".join(current_body).strip()))
                current_body = []
            current_title = re.sub(r"^#{1,6}\s+", "", line).strip()
        else:
            current_body.append(line)
    if current_body:
        sections.append((current_title, "\n".join(current_body).strip()))
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


# --------------------------------------------------------------------------- #
# Core ingestion
# --------------------------------------------------------------------------- #
def discover_package(zip_path: str | None) -> Path:
    """Ensure the package is extracted into data/base-knowledge/ and return it."""
    BASE_KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    if zip_path:
        zp = Path(zip_path).expanduser().resolve()
        if not zp.exists():
            raise FileNotFoundError(f"ZIP not found: {zp}")
        print(f"[ingest] extracting {zp.name} -> {BASE_KNOWLEDGE_DIR}")
        with zipfile.ZipFile(zp) as z:
            z.extractall(BASE_KNOWLEDGE_DIR)
    else:
        print(f"[ingest] no --zip given; using existing {BASE_KNOWLEDGE_DIR}")
    return BASE_KNOWLEDGE_DIR


def iter_files(base: Path) -> Iterable[Path]:
    for p in sorted(base.rglob("*")):
        if p.is_file() and not p.name.startswith("."):
            yield p


def ingest(base: Path) -> tuple[list[dict], list[dict]]:
    """Return (chunks, registry_entries)."""
    chunks: list[dict] = []
    registry: list[dict] = []
    counter = 0
    total_redactions = 0
    total_reclassified = 0

    for path in iter_files(base):
        rel = path.relative_to(base).as_posix()
        suffix = path.suffix.lower()
        doc_type, domain, sensitivity = _profile_for(path.name)
        size = path.stat().st_size
        sha = hashlib.sha256(path.read_bytes()).hexdigest()[:16]

        entry = {
            "source_file": rel,
            "file_type": suffix.lstrip("."),
            "document_type": doc_type,
            "knowledge_domain": domain,
            "sensitivity_level": sensitivity,
            "size_bytes": size,
            "sha256_16": sha,
            "ingested_at": _now(),
            "chunk_count": 0,
        }

        text = ""
        if suffix == ".docx":
            text = extract_docx_text(path)
        elif suffix in (".md", ".txt"):
            text = path.read_text("utf-8", "ignore")
        elif suffix in (".geojson", ".json", ".kml"):
            # Geospatial reference: index a safe descriptor only, never raw coords.
            entry["document_type"] = "geospatial"
            entry["knowledge_domain"] = "geospatial"
            entry["sensitivity_level"] = "RESTRICTED"
            text = (
                f"Geospatial reference: {path.name}. Describes the controlled MVP "
                "study area (approximately 180 km2 pilot zone) derived from "
                "protected geospatial references. Exact coordinates are held in "
                "restricted storage only and are never exposed through public, "
                "partner, or general knowledge surfaces."
            )
            # Preserve the ORIGINAL coordinate file only in restricted storage.
            GEO_DIR.mkdir(parents=True, exist_ok=True)
            _preserve_restricted_geospatial(path)
        elif suffix in (".png", ".jpg", ".jpeg"):
            entry["document_type"] = "figure"
            entry["knowledge_domain"] = "technical"
            text = (
                f"Supporting figure: {path.name}. "
                "Visual diagram included in the base knowledge package."
            )
        else:
            registry.append(entry)
            continue

        # Chunk text content.
        produced = 0
        doc_redactions = 0
        doc_reclassified = 0
        for section_title, body in split_into_sections(text):
            for piece in chunk_section(body):
                counter += 1
                sensitivity = entry["sensitivity_level"]

                # Redact any coordinate-like content and elevate sensitivity.
                content, n_redacted, _ = redact_coordinates(piece)
                if n_redacted:
                    elevated = elevated_level_for(piece, entry["document_type"])
                    if elevated != sensitivity:
                        doc_reclassified += 1
                        total_reclassified += 1
                    sensitivity = elevated
                    doc_redactions += n_redacted
                    total_redactions += n_redacted

                chunk = {
                    "chunk_id": f"KSM-KB-{counter:04d}",
                    "source_file": rel,
                    "document_type": entry["document_type"],
                    "section_title": section_title[:160],
                    "content": content,
                    "sensitivity_level": sensitivity,
                    "knowledge_domain": entry["knowledge_domain"],
                    "token_estimate": _estimate_tokens(content),
                    "created_at": _now(),
                    "redacted_coordinate_refs": n_redacted,
                    "needs_human_review": (
                        sensitivity in ("RESTRICTED", "HOUSE_OF_EARTH_TRUST_ONLY")
                        or n_redacted > 0
                    ),
                }
                chunks.append(chunk)
                produced += 1

        entry["chunk_count"] = produced
        entry["redacted_coordinate_refs"] = doc_redactions
        entry["reclassified_chunks"] = doc_reclassified
        registry.append(entry)
        flag = f" redacted={doc_redactions} reclassified={doc_reclassified}" if doc_redactions else ""
        print(f"[ingest] {rel:60s} {entry['file_type']:8s} chunks={produced}{flag}")

    print(
        f"[ingest] coordinate redaction: {total_redactions} reference(s) redacted, "
        f"{total_reclassified} chunk(s) reclassified."
    )
    return chunks, registry


def _preserve_restricted_geospatial(path: Path) -> None:
    """Copy an original GeoJSON/KML file into restricted storage (data/geo/).

    data/geo/ is gitignored, so raw coordinates live only in restricted local
    storage and are never committed or exposed through any knowledge surface.
    """
    import shutil

    target = GEO_DIR / path.name
    try:
        shutil.copy2(path, target)
    except OSError:
        pass


def write_outputs(chunks: list[dict], registry: list[dict]) -> None:
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    # 1. JSONL chunks
    jsonl = EXTRACTED_DIR / "knowledge_chunks.jsonl"
    with jsonl.open("w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    # 2. Document registry
    total_redacted = sum(d.get("redacted_coordinate_refs", 0) for d in registry)
    total_reclassified = sum(d.get("reclassified_chunks", 0) for d in registry)
    (EXTRACTED_DIR / "document_registry.json").write_text(
        json.dumps(
            {
                "generated_at": _now(),
                "document_count": len(registry),
                "chunk_count": len(chunks),
                "redacted_coordinate_refs": total_redacted,
                "reclassified_chunks": total_reclassified,
                "documents": registry,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # 3. Human-readable summary
    by_domain: dict[str, int] = {}
    by_sensitivity: dict[str, int] = {}
    by_type: dict[str, int] = {}
    for c in chunks:
        by_domain[c["knowledge_domain"]] = by_domain.get(c["knowledge_domain"], 0) + 1
        by_sensitivity[c["sensitivity_level"]] = (
            by_sensitivity.get(c["sensitivity_level"], 0) + 1
        )
    for d in registry:
        by_type[d["document_type"]] = by_type.get(d["document_type"], 0) + 1

    lines = [
        "# KASAMOR Knowledge Index Summary",
        "",
        f"_Generated: {_now()}_",
        "",
        f"- **Documents ingested:** {len(registry)}",
        f"- **Knowledge chunks:** {len(chunks)}",
        f"- **Coordinate references redacted:** {total_redacted}",
        f"- **Chunks reclassified by redaction:** {total_reclassified}",
        "",
        "## Chunks by knowledge domain",
        "",
    ]
    for k in sorted(by_domain):
        lines.append(f"- `{k}`: {by_domain[k]}")
    lines += ["", "## Chunks by sensitivity level", ""]
    for k in sorted(by_sensitivity):
        lines.append(f"- `{k}`: {by_sensitivity[k]}")
    lines += ["", "## Documents by type", ""]
    for k in sorted(by_type):
        lines.append(f"- `{k}`: {by_type[k]}")
    lines += [
        "",
        "## Documents",
        "",
        "| Source file | Type | Domain | Sensitivity | Chunks |",
        "|---|---|---|---|---|",
    ]
    for d in registry:
        lines.append(
            f"| {d['source_file']} | {d['document_type']} | "
            f"{d['knowledge_domain']} | {d['sensitivity_level']} | {d['chunk_count']} |"
        )
    lines += [
        "",
        "> Note: geospatial files are indexed as RESTRICTED descriptors only, and "
        "their original coordinate files are preserved exclusively in restricted "
        "storage (`data/geo/`, gitignored). Any latitude/longitude values, GeoJSON "
        "coordinate arrays, KML coordinate strings, or AOI center references found "
        "in document prose are automatically redacted to "
        "`[RESTRICTED_COORDINATE]` / `[PROTECTED_GEOSPATIAL_REFERENCE]` and the "
        "owning chunk is elevated to RESTRICTED (or HOUSE_OF_EARTH_TRUST_ONLY for "
        "private expert/evidence context). Raw coordinates are never written to "
        "PUBLIC, PARTNER, or INTERNAL chunks.",
        "",
    ]
    (EXTRACTED_DIR / "knowledge_index_summary.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print(f"\n[ingest] wrote {jsonl}")
    print(f"[ingest] wrote {EXTRACTED_DIR / 'document_registry.json'}")
    print(f"[ingest] wrote {EXTRACTED_DIR / 'knowledge_index_summary.md'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest KASAMOR base knowledge package.")
    parser.add_argument("--zip", help="Path to the clean base knowledge ZIP package.")
    args = parser.parse_args()

    base = discover_package(args.zip)
    chunks, registry = ingest(base)
    if not chunks:
        print(
            "[ingest] WARNING: no chunks produced. "
            "Provide --zip pointing at the clean package, or place documents in "
            f"{BASE_KNOWLEDGE_DIR}."
        )
    write_outputs(chunks, registry)
    print(
        f"\n[ingest] done: {len(registry)} documents, {len(chunks)} chunks.\n"
    )


if __name__ == "__main__":
    main()
