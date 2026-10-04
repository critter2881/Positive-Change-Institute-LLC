"""
Prometheus orchestration service.

Routes a task to one or more AI providers with:

* ordered fallback (OpenAI, then Grok) when a provider fails,
* bounded retries with exponential backoff,
* an optional cross-check mode that asks every configured provider and flags
  disagreement for human review,
* a structured audit record for every decision (logger ``prometheus.audit``).

Provider calls never raise: failures are reported in the result.
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Callable, Optional

import requests

audit_logger = logging.getLogger("prometheus.audit")
logger = logging.getLogger(__name__)

_TIMEOUT = 20
_MAX_ATTEMPTS = 3
_BACKOFF_SECONDS = 0.5
_RETRYABLE = {429, 500, 502, 503, 504}

PROVIDERS = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4o",
        "env": "OPENAI_API_KEY",
    },
    "grok": {
        "url": "https://api.x.ai/v1/chat/completions",
        "model": "grok-3",
        "env": "GROK_API_KEY",
    },
}
PROVIDER_ORDER = ("openai", "grok")


def _system_prompt(division: str) -> str:
    return (
        "You are Prometheus, the AI orchestrator for Positive Change Institute LLC. "
        f"You are managing the '{division or 'all divisions'}' vertical. "
        "Respond with actionable intelligence in 1-3 concise sentences."
    )


def call_provider(
    name: str,
    task: str,
    division: str,
    api_key: str,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """Call one provider with retries. Returns ``{ok, model, result|error, attempts}``."""
    spec = PROVIDERS[name]
    payload = {
        "model": spec["model"],
        "messages": [
            {"role": "system", "content": _system_prompt(division)},
            {"role": "user", "content": task},
        ],
        "max_tokens": 256,
    }
    error = "unknown error"
    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            resp = requests.post(
                spec["url"],
                headers={"Authorization": "Bearer " + api_key},
                json=payload,
                timeout=_TIMEOUT,
            )
            if resp.status_code in _RETRYABLE:
                error = f"HTTP {resp.status_code}"
            else:
                resp.raise_for_status()
                data = resp.json()
                choices = data.get("choices") if isinstance(data, dict) else None
                message = (
                    choices[0].get("message")
                    if isinstance(choices, list)
                    and choices
                    and isinstance(choices[0], dict)
                    else None
                )
                content = message.get("content") if isinstance(message, dict) else None
                if not isinstance(content, str) or not content.strip():
                    raise ValueError("invalid provider response")
                content = content.strip()
                return {
                    "ok": True,
                    "provider": name,
                    "model": spec["model"],
                    "result": content,
                    "attempts": attempt,
                }
        except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
            error = type(exc).__name__
            if isinstance(exc, requests.HTTPError):
                break  # non-retryable client error
        if attempt < _MAX_ATTEMPTS:
            sleep(_BACKOFF_SECONDS * 2 ** (attempt - 1))
    logger.error("Provider %s failed after retries: %s", name, error)
    return {
        "ok": False,
        "provider": name,
        "model": spec["model"],
        "error": error,
        "attempts": attempt,
    }


def _tokens(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def agreement(a: str, b: str) -> float:
    """Jaccard similarity of word sets, in [0, 1]."""
    ta, tb = _tokens(a), _tokens(b)
    if not ta and not tb:
        return 1.0
    return len(ta & tb) / len(ta | tb)


def _audit(record: dict) -> None:
    audit_logger.info(json.dumps(record, sort_keys=True))


def execute(
    task: str,
    division: str,
    keys: dict,
    cross_check: bool = False,
    agreement_threshold: float = 0.3,
    sleep: Callable[[float], None] = time.sleep,
) -> dict:
    """
    Route *task* using the keys in *keys* (``{"openai": ..., "grok": ...}``).

    Returns ``{result, model, mode, ...}``. With no keys the result is a demo
    response and ``model`` is ``"demo"``.
    """
    configured = [p for p in PROVIDER_ORDER if keys.get(p)]
    started = time.time()

    if not configured:
        outcome = {
            "result": (
                f"[DEMO] Prometheus would route '{task}' for division "
                f"'{division or 'all'}' to the optimal intelligence layer. "
                "Set OPENAI_API_KEY or GROK_API_KEY to enable live AI routing."
            ),
            "model": "demo",
            "mode": "demo",
            "attempted": [],
        }
        _audit({"event": "prometheus.route", "division": division or "all",
                "mode": "demo", "task_chars": len(task)})
        return outcome

    attempts: list = []
    answers: list = []
    for name in configured:
        res = call_provider(name, task, division, keys[name], sleep=sleep)
        attempts.append(
            {k: res[k] for k in ("provider", "model", "ok", "attempts")}
        )
        if res["ok"]:
            answers.append(res)
            if not cross_check:
                break  # first healthy provider wins (ordered fallback)

    outcome: dict = {"attempted": attempts}
    if not answers:
        outcome.update(
            result="AI routing is temporarily unavailable.",
            model=PROVIDERS[configured[0]]["model"],
            mode="failed",
        )
    elif cross_check:
        primary = answers[0]
        outcome.update(result=primary["result"], model=primary["model"], mode="cross_check")
        if len(answers) > 1:
            score = round(agreement(answers[0]["result"], answers[1]["result"]), 3)
            outcome["cross_check"] = {
                "providers": [a["provider"] for a in answers],
                "agreement": score,
                "needs_review": score < agreement_threshold,
                "alternate_result": answers[1]["result"],
            }
        else:
            outcome["cross_check"] = {
                "providers": [answers[0]["provider"]],
                "agreement": None,
                "needs_review": True,
                "note": "Only one provider answered; no cross-check possible.",
            }
    else:
        outcome.update(
            result=answers[0]["result"],
            model=answers[0]["model"],
            mode="fallback" if attempts[0]["provider"] != answers[0]["provider"] else "primary",
        )

    _audit(
        {
            "event": "prometheus.route",
            "division": division or "all",
            "mode": outcome["mode"],
            "model": outcome["model"],
            "attempts": attempts,
            "needs_review": (outcome.get("cross_check") or {}).get("needs_review"),
            "task_chars": len(task),
            "elapsed_ms": int((time.time() - started) * 1000),
        }
    )
    return outcome


def provider_keys(env_get: Callable[[str, str], Optional[str]]) -> dict:
    return {name: env_get(spec["env"], "") for name, spec in PROVIDERS.items()}
