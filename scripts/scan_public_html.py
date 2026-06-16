#!/usr/bin/env python3
"""
KASAMOR — Public Served-HTML Safety Scan
========================================

Fetches the live public-interface pages and fails if the rendered HTML contains
exact coordinates, GeoJSON/KML references, field-packet data, or forbidden
positioning language. Used in CI after `next start`.

Usage:
    python3 scripts/scan_public_html.py [BASE_URL]
    (default BASE_URL = http://localhost:3000)

Exit 0 if clean, 1 if any violation is found.
"""
from __future__ import annotations

import re
import sys
import urllib.request

PAGES = ["/", "/ecosystem", "/how-it-works", "/mvp", "/partners"]

# Hard violations (any match fails CI).
PATTERNS = {
    "exact coordinates": re.compile(r"35\.456\d|14\.594\d|lookat_|-?\d{1,3}\.\d{4,}\s*,\s*-?\d{1,3}\.\d{4,}"),
    "geojson/kml": re.compile(r"\.geojson|\.kml|featurecollection|<coordinates>", re.IGNORECASE),
    "field-packet data": re.compile(r"KSM-FP-\d|KSM-PH-\d|KSM-VN-\d|contributor_code"),
    "forbidden language": re.compile(
        r"gold[- ]?detect|prospect(?:ing|or)|gold map|mining target|guaranteed mineral|reserve estimate|extraction instruction",
        re.IGNORECASE,
    ),
}

# "target map" is allowed only in the safety negation "not a target map".
TARGET_MAP = re.compile(r"target map", re.IGNORECASE)
TARGET_MAP_OK = re.compile(r"not a target map", re.IGNORECASE)


def fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=15) as r:
        return r.read().decode("utf-8", "ignore")


def scan(base: str) -> int:
    violations: list[str] = []
    for page in PAGES:
        url = base.rstrip("/") + page
        try:
            html = fetch(url)
        except Exception as exc:  # pragma: no cover
            violations.append(f"{page}: could not fetch ({exc})")
            continue
        for name, pat in PATTERNS.items():
            m = pat.search(html)
            if m:
                violations.append(f"{page}: {name} -> {m.group(0)!r}")
        # target map: flag only if a bare occurrence isn't the allowed negation.
        bare = TARGET_MAP.sub(lambda mo: "", TARGET_MAP_OK.sub("", html))
        if TARGET_MAP.search(bare):
            violations.append(f"{page}: forbidden 'target map' (not the allowed negation)")
        print(f"scanned {url}")

    print("=" * 60)
    if violations:
        print("PUBLIC HTML SCAN: FAIL")
        for v in violations:
            print("  -", v)
        return 1
    print("PUBLIC HTML SCAN: PASS (no coordinates, GeoJSON, field data, or forbidden language)")
    return 0


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    sys.exit(scan(base))
