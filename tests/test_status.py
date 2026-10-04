"""Tests for the plain-language status report."""

from scripts import status


def test_report_has_key_lines():
    report = status.build_report()
    for label in ("PCI STATUS", "Branch:", "Quant verification:", "Open tasks:", "make check"):
        assert label in report


def test_open_tasks_reads_checklist():
    assert all(isinstance(t, str) for t in status.open_tasks())
