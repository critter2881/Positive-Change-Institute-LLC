"""Every division in the registry must have a profile page."""

import json
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_PAGES = _ROOT / "docs" / "guide" / "divisions"


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def test_every_division_has_profile():
    registry = json.loads((_ROOT / "config" / "divisions_registry.json").read_text())
    for index, division in enumerate(registry, 1):
        page = _PAGES / f"{index:02d}-{_slug(division['name'])}.md"
        assert page.is_file(), f"Missing profile: {page.name}"
        text = page.read_text()
        for product_id in division["product_ids"]:
            assert product_id in text, f"{product_id} missing in {page.name}"
