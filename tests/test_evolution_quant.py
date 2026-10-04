"""Tests for the auto-evolution engine and quant verification."""

import datetime

import pytest

from arcana_enterprise_nfts.arcana_nfts import arcana_nfts
from arcana_enterprise_nfts.evolution.engine import evolve
from scripts.quant_verify import rotating_seed, verify

FORGE = next(n for n in arcana_nfts if n["product_id"] == "FORGE-001")


def test_evolution_levels_and_traits_accumulate():
    assert evolve(FORGE, 0)["level"] == 1
    assert evolve(FORGE, 100)["level"] == 2
    top = evolve(FORGE, 10_000)
    assert top["level"] == 3 and top["next_level_at"] is None
    assert "Core glyph set" in top["traits"]


def test_negative_score_rejected():
    with pytest.raises(ValueError):
        evolve(FORGE, -1)


def test_non_evolving_nft():
    assert evolve({"product_id": "X", "auto_evolution": False}, 999)["evolving"] is False


def test_rotating_seed_changes_weekly():
    a = rotating_seed(datetime.date(2026, 1, 5))
    assert a == rotating_seed(datetime.date(2026, 1, 11))
    assert a != rotating_seed(datetime.date(2026, 1, 12))


def test_quant_verification_passes_and_is_reproducible():
    first = verify(seed=1, samples=50)
    assert first["verified"], first["failures"]
    assert first == verify(seed=1, samples=50)


def test_evolve_endpoint(client):
    data = client.get("/api/nft/collections/FORGE-001/evolve?score=150").get_json()
    assert data["level"] == 2
    assert client.get("/api/nft/collections/NOPE/evolve").status_code == 404
    assert client.get("/api/nft/collections/FORGE-001/evolve?score=x").status_code == 400
