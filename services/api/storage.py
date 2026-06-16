"""
KASAMOR API — Local JSON storage
================================

Dead-simple file-backed storage for the MVP. No database required. Field packets
live in data/field-packets/, review decisions in data/review/, knowledge index in
data/extracted-knowledge/.

A future sprint can swap this module for a PostgreSQL/PostGIS-backed repository
without changing the route handlers.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FIELD_PACKETS_DIR = DATA / "field-packets"
MEDIA_DIR = DATA / "media"
REVIEW_DIR = DATA / "review"
EXTRACTED_DIR = DATA / "extracted-knowledge"
OUTPUTS_DIR = DATA / "outputs"


def _read_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Field packets — one JSON file per packet, plus the bundled sample.
# --------------------------------------------------------------------------- #
def list_field_packets() -> list[dict]:
    packets: dict[str, dict] = {}
    if FIELD_PACKETS_DIR.exists():
        for p in sorted(FIELD_PACKETS_DIR.glob("*.json")):
            data = _read_json(p, None)
            if isinstance(data, dict) and "field_packet_id" in data:
                packets[data["field_packet_id"]] = data
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "field_packet_id" in item:
                        packets[item["field_packet_id"]] = item
    return list(packets.values())


def get_field_packet(packet_id: str) -> dict | None:
    for pk in list_field_packets():
        if pk["field_packet_id"] == packet_id:
            return pk
    return None


def save_field_packet(packet: dict) -> dict:
    FIELD_PACKETS_DIR.mkdir(parents=True, exist_ok=True)
    path = FIELD_PACKETS_DIR / f"{packet['field_packet_id']}.json"
    _write_json(path, packet)
    return packet


def next_field_packet_id() -> str:
    existing = [pk["field_packet_id"] for pk in list_field_packets()]
    nums = [int(x.split("-")[-1]) for x in existing if x.startswith("KSM-FP-")]
    return f"KSM-FP-{(max(nums) + 1) if nums else 1:04d}"


# --------------------------------------------------------------------------- #
# Media (photo + voice metadata)
# --------------------------------------------------------------------------- #
def list_photo_metadata() -> list[dict]:
    out: list[dict] = []
    for p in sorted(MEDIA_DIR.glob("*photo*.json")) if MEDIA_DIR.exists() else []:
        data = _read_json(p, [])
        out.extend(data if isinstance(data, list) else [data])
    return out


def list_voice_notes() -> list[dict]:
    out: list[dict] = []
    for p in sorted(MEDIA_DIR.glob("*voice*.json")) if MEDIA_DIR.exists() else []:
        data = _read_json(p, [])
        out.extend(data if isinstance(data, list) else [data])
    return out


def photos_for_packet(packet_id: str) -> list[dict]:
    return [m for m in list_photo_metadata() if m.get("field_packet_id") == packet_id]


def voice_notes_for_packet(packet_id: str) -> list[dict]:
    return [m for m in list_voice_notes() if m.get("field_packet_id") == packet_id]


# --------------------------------------------------------------------------- #
# Review decisions
# --------------------------------------------------------------------------- #
def list_reviews() -> list[dict]:
    path = REVIEW_DIR / "review_decisions.json"
    data = _read_json(path, [])
    return data if isinstance(data, list) else []


def add_review(decision: dict) -> dict:
    path = REVIEW_DIR / "review_decisions.json"
    data = list_reviews()
    data.append(decision)
    _write_json(path, data)
    return decision


# --------------------------------------------------------------------------- #
# Knowledge index
# --------------------------------------------------------------------------- #
def load_document_registry() -> dict | None:
    return _read_json(EXTRACTED_DIR / "document_registry.json", None)


def load_chunks() -> list[dict]:
    path = EXTRACTED_DIR / "knowledge_chunks.jsonl"
    if not path.exists():
        return []
    out: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
