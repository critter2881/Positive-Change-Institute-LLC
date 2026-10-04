"""
Auto-evolution engine for Arcana Enterprise NFTs.

Deterministic: the same catalog entry and activity score always produce the
same level. Levels come from each entry's ``evolution_paths``; a level unlocks
when the score reaches its threshold.
"""

from __future__ import annotations

# Minimum activity score required for each evolution level.
LEVEL_THRESHOLDS = {1: 0, 2: 100, 3: 500}


def evolve(nft: dict, score: float) -> dict:
    """Return the evolution state of *nft* for the given activity *score*."""
    if score < 0:
        raise ValueError("score must be non-negative")
    paths = sorted(nft.get("evolution_paths", []), key=lambda p: p["level"])
    if not nft.get("auto_evolution") or not paths:
        return {
            "product_id": nft.get("product_id"),
            "evolving": False,
            "level": None,
            "traits": [],
            "next_level_at": None,
        }

    current = paths[0]
    for path in paths:
        if score >= LEVEL_THRESHOLDS.get(path["level"], float("inf")):
            current = path
    traits: list = []
    for path in paths:
        if path["level"] <= current["level"]:
            traits.extend(path["traits"])
    later = [
        LEVEL_THRESHOLDS[p["level"]]
        for p in paths
        if p["level"] > current["level"] and p["level"] in LEVEL_THRESHOLDS
    ]
    return {
        "product_id": nft.get("product_id"),
        "evolving": True,
        "level": current["level"],
        "traits": traits,
        "next_level_at": min(later) if later else None,
    }
