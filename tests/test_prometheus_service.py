"""Tests for the Prometheus multi-model router."""

import json
import logging
from unittest.mock import MagicMock

import requests

from backend.services import prometheus as prom


def _ok(text):
    r = MagicMock()
    r.status_code = 200
    r.raise_for_status.return_value = None
    r.json.return_value = {"choices": [{"message": {"content": text}}]}
    return r


def _status(code):
    r = MagicMock()
    r.status_code = code
    r.raise_for_status.side_effect = requests.HTTPError(str(code))
    return r


def _router(monkeypatch, responses):
    """Patch requests.post: *responses* maps URL substring -> list of replies."""
    calls = []

    def fake_post(url, **kwargs):
        calls.append(url)
        for key, queue in responses.items():
            if key in url:
                item = queue.pop(0) if len(queue) > 1 else queue[0]
                if isinstance(item, Exception):
                    raise item
                return item
        raise AssertionError(url)

    monkeypatch.setattr(prom.requests, "post", fake_post)
    return calls


NOSLEEP = lambda s: None  # noqa: E731


def test_demo_mode_without_keys():
    out = prom.execute("t", "", {}, sleep=NOSLEEP)
    assert out["model"] == "demo" and out["mode"] == "demo"


def test_primary_provider_used(monkeypatch):
    _router(monkeypatch, {"openai": [_ok("alpha")]})
    out = prom.execute("t", "", {"openai": "k", "grok": "k"}, sleep=NOSLEEP)
    assert (out["mode"], out["result"], out["model"]) == ("primary", "alpha", "gpt-4o")


def test_retries_then_succeeds(monkeypatch):
    calls = _router(monkeypatch, {"openai": [_status(503), _status(503), _ok("late")]})
    out = prom.execute("t", "", {"openai": "k"}, sleep=NOSLEEP)
    assert out["result"] == "late"
    assert len(calls) == 3


def test_falls_back_to_grok(monkeypatch):
    _router(monkeypatch, {"openai": [requests.ConnectionError()], "x.ai": [_ok("beta")]})
    out = prom.execute("t", "", {"openai": "k", "grok": "k"}, sleep=NOSLEEP)
    assert out["mode"] == "fallback" and out["model"] == "grok-3"


def test_client_error_not_retried(monkeypatch):
    calls = _router(monkeypatch, {"openai": [_status(401)]})
    out = prom.execute("t", "", {"openai": "k"}, sleep=NOSLEEP)
    assert out["mode"] == "failed" and len(calls) == 1


def test_all_fail_is_graceful(monkeypatch):
    _router(monkeypatch, {"openai": [_status(500)], "x.ai": [_status(500)]})
    out = prom.execute("t", "", {"openai": "k", "grok": "k"}, sleep=NOSLEEP)
    assert out["mode"] == "failed"
    assert "unavailable" in out["result"]


def test_cross_check_agreement(monkeypatch):
    _router(monkeypatch, {"openai": [_ok("raise the pool depth")],
                          "x.ai": [_ok("raise the pool depth")]})
    out = prom.execute("t", "", {"openai": "k", "grok": "k"}, cross_check=True, sleep=NOSLEEP)
    assert out["cross_check"]["agreement"] == 1.0
    assert out["cross_check"]["needs_review"] is False


def test_cross_check_disagreement_flagged(monkeypatch):
    _router(monkeypatch, {"openai": [_ok("buy everything now")],
                          "x.ai": [_ok("sell holdings immediately")]})
    out = prom.execute("t", "", {"openai": "k", "grok": "k"}, cross_check=True, sleep=NOSLEEP)
    assert out["cross_check"]["needs_review"] is True


def test_cross_check_single_provider_needs_review(monkeypatch):
    _router(monkeypatch, {"openai": [_ok("x")]})
    out = prom.execute("t", "", {"openai": "k"}, cross_check=True, sleep=NOSLEEP)
    assert out["cross_check"]["needs_review"] is True


def test_audit_record_written_without_secrets(monkeypatch, caplog):
    _router(monkeypatch, {"openai": [_ok("alpha")]})
    with caplog.at_level(logging.INFO, logger="prometheus.audit"):
        prom.execute("secret task text", "XRPL", {"openai": "sk-SECRET"}, sleep=NOSLEEP)
    record = json.loads(caplog.records[-1].message)
    assert record["mode"] == "primary" and record["division"] == "XRPL"
    assert "sk-SECRET" not in caplog.text and "secret task text" not in caplog.text


def test_agreement_bounds():
    assert prom.agreement("", "") == 1.0
    assert prom.agreement("a b", "c d") == 0.0
