"""
KASAMOR — Data Sensitivity Model
================================

Five sensitivity levels gate every piece of data in the ecosystem. This module
is the single source of truth for the levels, their ordering, and the rules that
decide what each surface (public interface vs. internal console) may render.

See docs/data-governance.md for the human-readable policy.
"""
from __future__ import annotations

from enum import Enum


class SensitivityLevel(str, Enum):
    PUBLIC = "PUBLIC"
    PARTNER = "PARTNER"
    INTERNAL = "INTERNAL"
    RESTRICTED = "RESTRICTED"
    HOUSE_OF_EARTH_TRUST_ONLY = "HOUSE_OF_EARTH_TRUST_ONLY"


# Numeric ordering: a surface cleared at level N may render data at level <= N.
ORDER: dict[str, int] = {
    SensitivityLevel.PUBLIC: 0,
    SensitivityLevel.PARTNER: 1,
    SensitivityLevel.INTERNAL: 2,
    SensitivityLevel.RESTRICTED: 3,
    SensitivityLevel.HOUSE_OF_EARTH_TRUST_ONLY: 4,
}


# What each consuming surface is cleared to see.
SURFACE_CLEARANCE: dict[str, SensitivityLevel] = {
    # Public interface: PUBLIC only. PARTNER content must be hand-curated, never
    # served wholesale, so the public API ceiling stays at PUBLIC.
    "public": SensitivityLevel.PUBLIC,
    "partner": SensitivityLevel.PARTNER,
    "internal": SensitivityLevel.INTERNAL,
    "trust": SensitivityLevel.HOUSE_OF_EARTH_TRUST_ONLY,
}


def level_value(level: str | SensitivityLevel) -> int:
    return ORDER.get(SensitivityLevel(level), ORDER[SensitivityLevel.INTERNAL])


def can_view(data_level: str | SensitivityLevel, clearance: str | SensitivityLevel) -> bool:
    """True if a surface with `clearance` may render data at `data_level`."""
    return level_value(data_level) <= level_value(clearance)


def is_publicly_safe(data_level: str | SensitivityLevel) -> bool:
    """Only PUBLIC content is ever auto-served publicly."""
    return SensitivityLevel(data_level) == SensitivityLevel.PUBLIC


# Fields that must NEVER leave the internal boundary, regardless of level.
NEVER_PUBLIC_FIELDS = frozenset(
    {
        "lat",
        "lon",
        "accuracy_m",
        "location",
        "coordinates",
        "contributor_code",
        "raw_audio",
        "raw_photo",
        "transcript",
    }
)


def redact_for_public(obj: dict) -> dict:
    """Return a shallow copy with never-public fields removed. Defensive helper
    for any code path that might otherwise serialise sensitive data publicly."""
    return {k: v for k, v in obj.items() if k not in NEVER_PUBLIC_FIELDS}
