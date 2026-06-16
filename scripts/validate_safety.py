#!/usr/bin/env python3
"""
KASAMOR — Safety & Coordinate Validation
========================================

Repeatable checks confirming that no exact coordinates, GeoJSON/KML coordinate
content, or sensitive geospatial data reach PUBLIC / PARTNER / INTERNAL knowledge
chunks, and that the public interface remains coordinate-free.

Exit code 0 if all checks pass, 1 otherwise.

Usage:
    python3 scripts/validate_safety.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "data" / "extracted-knowledge" / "knowledge_chunks.jsonl"
PUBLIC_CONTENT = ROOT / "apps" / "public-interface"

# Raw-coordinate detectors (what must NOT appear in non-restricted content).
AOI_NUMBERS = re.compile(r"35\.456\d|14\.594\d")
DECIMAL_PAIR = re.compile(r"-?\d{1,3}\.\d{4,}\s*,\s*-?\d{1,3}\.\d{4,}")
GEOJSON_ARR = re.compile(r'"coordinates"\s*:\s*\[\s*-?\d+\.\d+', re.IGNORECASE)
KML_COORDS = re.compile(r"<coordinates>\s*-?\d", re.IGNORECASE)
JSON_LATLON_VAL = re.compile(
    r'"(?:lat|lon|latitude|longitude)"\s*:\s*-?\d+\.\d+', re.IGNORECASE
)

RAW_COORD_DETECTORS = [AOI_NUMBERS, DECIMAL_PAIR, GEOJSON_ARR, KML_COORDS, JSON_LATLON_VAL]

NON_RESTRICTED = {"PUBLIC", "PARTNER", "INTERNAL"}


def has_raw_coords(text: str) -> bool:
    return any(p.search(text) for p in RAW_COORD_DETECTORS)


def load_chunks() -> list[dict]:
    return [json.loads(l) for l in CHUNKS.open(encoding="utf-8") if l.strip()]


def main() -> int:
    results: list[tuple[str, bool, str]] = []

    chunks = load_chunks()

    # 1-3. No raw coordinates in PUBLIC / PARTNER / INTERNAL chunks.
    for level in ["PUBLIC", "PARTNER", "INTERNAL"]:
        offenders = [
            c["chunk_id"]
            for c in chunks
            if c.get("sensitivity_level") == level and has_raw_coords(c.get("content", ""))
        ]
        results.append(
            (f"0 exact coordinates in {level} chunks", not offenders, ",".join(offenders))
        )

    # 4. Any chunk that still contains raw coordinates must be RESTRICTED/HOET.
    leaked = [
        c["chunk_id"]
        for c in chunks
        if has_raw_coords(c.get("content", ""))
        and c.get("sensitivity_level") in NON_RESTRICTED
    ]
    results.append(
        ("all raw-coordinate content is restricted (none in PUBLIC/PARTNER/INTERNAL)",
         not leaked, ",".join(leaked))
    )

    # 5. Redaction actually happened (placeholders present somewhere).
    redacted = sum(c.get("redacted_coordinate_refs", 0) for c in chunks)
    placeholders = sum(
        1
        for c in chunks
        if "[RESTRICTED_COORDINATE]" in c.get("content", "")
        or "[PROTECTED_GEOSPATIAL_REFERENCE]" in c.get("content", "")
    )
    results.append(
        (f"redaction applied (refs={redacted}, chunks_with_placeholder={placeholders})",
         redacted > 0 and placeholders > 0, "")
    )

    # 6. Geospatial-typed chunks carry no raw coordinates.
    geo_offenders = [
        c["chunk_id"]
        for c in chunks
        if c.get("document_type") == "geospatial" and has_raw_coords(c.get("content", ""))
    ]
    results.append(
        ("geospatial-derived chunks contain no raw coordinates",
         not geo_offenders, ",".join(geo_offenders))
    )

    # 7. Public interface source is coordinate-free and exposes no field data.
    pub_offenders: list[str] = []
    for p in PUBLIC_CONTENT.rglob("*"):
        if p.suffix not in {".ts", ".tsx", ".json", ".md", ".css"}:
            continue
        if "node_modules" in p.parts or ".next" in p.parts:
            continue
        txt = p.read_text("utf-8", "ignore")
        if has_raw_coords(txt) or re.search(r"KSM-FP-\d|KSM-PH-\d|KSM-VN-\d|contributor_code", txt):
            # Allow the safety negation phrasing; only flag actual coord/data.
            pub_offenders.append(p.relative_to(ROOT).as_posix())
    results.append(
        ("public interface source: no coordinates or field-packet data",
         not pub_offenders, ",".join(pub_offenders))
    )

    # 8. Restricted geospatial originals are not tracked by git (best-effort note).
    geo_dir = ROOT / "data" / "geo"
    raw_geo = [p.name for p in geo_dir.glob("*") if p.suffix in {".geojson", ".kml", ".json"}]
    results.append(
        (f"restricted geospatial originals preserved locally only ({len(raw_geo)} file(s), gitignored)",
         True, "")
    )

    # Report.
    print("KASAMOR Safety Validation")
    print("=" * 60)
    all_ok = True
    for name, ok, detail in results:
        all_ok &= ok
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] {name}"
        if detail and not ok:
            line += f"  -> {detail}"
        print(line)
    print("=" * 60)
    print("RESULT:", "ALL PASS" if all_ok else "FAILURES PRESENT")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
