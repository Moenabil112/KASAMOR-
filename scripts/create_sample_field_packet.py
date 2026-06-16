#!/usr/bin/env python3
"""
KASAMOR — Create a sample Field Packet
======================================

Generates a new, valid Field Packet JSON file under data/field-packets/ with the
next available KSM-FP id. Useful for demos and for testing the API/console with
more than one packet.

Coordinates are written as RESTRICTED and are placeholder values within the
general MVP study area — never precise operational targets.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKETS = ROOT / "data" / "field-packets"


def _next_id() -> str:
    PACKETS.mkdir(parents=True, exist_ok=True)
    nums = []
    for p in PACKETS.glob("*.json"):
        try:
            data = json.loads(p.read_text("utf-8"))
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            fid = it.get("field_packet_id", "")
            if fid.startswith("KSM-FP-"):
                nums.append(int(fid.split("-")[-1]))
    return f"KSM-FP-{(max(nums) + 1) if nums else 1:04d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a sample Field Packet.")
    parser.add_argument("--contributor", default="FIELD-002")
    parser.add_argument("--place", default="Lower drainage fan, eastern sector")
    parser.add_argument("--season", default="dry_season")
    args = parser.parse_args()

    packet_id = _next_id()
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    packet = {
        "field_packet_id": packet_id,
        "contributor_code": args.contributor,
        "location": {
            "lat": 14.5901,
            "lon": 35.4602,
            "accuracy_m": 12,
            "sensitivity_level": "RESTRICTED",
        },
        "place_label": args.place,
        "observation_date": _dt.date.today().isoformat(),
        "seasonal_context": args.season,
        "photos": [],
        "voice_notes": [],
        "local_notes": ["Dry channel now; contributor recalls flow last season."],
        "sediment_observations": ["Pale sand dominant; little dark material visible when dry."],
        "rock_observations": ["Scattered weathered rock along the fan edge."],
        "water_drainage_observations": ["Broad shallow fan; no active flow at visit."],
        "observation_tags": ["dry_season", "drainage_fan"],
        "ai_summary": None,
        "review_status": "pending",
        "review_decision": None,
        "created_at": now,
    }

    out = PACKETS / f"{packet_id}.json"
    out.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[create] wrote {out}")


if __name__ == "__main__":
    main()
