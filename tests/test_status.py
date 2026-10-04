"""Tests for the plain-language status report."""

from scripts import status


def test_report_has_key_lines():
    report = status.build_report()
    for label in ("PCI STATUS", "Branch:", "Quant verification:", "Open tasks:", "make check"):
        assert label in report


def test_open_tasks_reads_checklist():
    assert all(isinstance(t, str) for t in status.open_tasks())


def test_last_change_skips_unreleased_heading(tmp_path, monkeypatch):
    (tmp_path / "CHANGELOG.md").write_text(
        "## [Unreleased]\n\n## [2.0.0]\n", encoding="utf-8"
    )
    monkeypatch.setattr(status, "_ROOT", tmp_path)
    assert status.last_change() == "[2.0.0]"
