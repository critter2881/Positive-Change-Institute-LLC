"""Tests for the APO measurement harness."""

from scripts import apo_measure


def test_measure_small_run():
    r = apo_measure.measure(40)
    assert r["failures"] == 0
    assert r["corruption_detected"] is True
    # 40 requests cannot support a 99.997% claim: honesty check.
    assert r["supports_claimed_integrity"] is False
    assert r["not_measurable_here"]


def test_percentile():
    assert apo_measure.percentile([1, 2, 3, 4], 100) == 4
