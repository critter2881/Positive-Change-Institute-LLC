"""Accessibility baseline checks for the static frontend (WCAG-oriented)."""

import re
from pathlib import Path

_HTML = (Path(__file__).resolve().parent.parent / "frontend" / "index.html").read_text()


def test_language_declared():
    assert re.search(r"<html[^>]+lang=\"[a-z]{2}", _HTML)


def test_skip_link_targets_main_landmark():
    assert 'href="#main"' in _HTML and '<main id="main">' in _HTML


def test_visible_keyboard_focus():
    assert ":focus-visible" in _HTML


def test_reduced_motion_respected():
    assert "prefers-reduced-motion" in _HTML


def test_images_have_alt_text():
    for tag in re.findall(r"<img\b[^>]*>", _HTML):
        assert "alt=" in tag, tag


def test_navigation_is_labeled():
    assert "aria-label=" in _HTML


def test_viewport_allows_zoom():
    assert "user-scalable=no" not in _HTML and "maximum-scale=1" not in _HTML
