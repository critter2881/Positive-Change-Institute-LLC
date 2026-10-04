#!/usr/bin/env python3
"""Plain-language "where am I?" summary, so nothing has to be remembered."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def _git(*args: str) -> str:
    try:
        out = subprocess.run(
            ["git", *args], cwd=_ROOT, capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def open_tasks() -> list:
    path = _ROOT / "tasks.md"
    if not path.is_file():
        return []
    return [
        line.strip()[6:]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("- [ ] ")
    ]


def last_change() -> str:
    path = _ROOT / "CHANGELOG.md"
    if not path.is_file():
        return "no changelog"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## ["):
            return line[3:].strip()
    return "no entries"


def last_verification() -> str:
    path = _ROOT / "reports" / "quant_verification.json"
    if not path.is_file():
        return "never run: type `make verify`"
    data = json.loads(path.read_text(encoding="utf-8"))
    state = "PASSED" if data.get("verified") else "FAILED"
    return f"{state} (seed {data.get('seed')}, {data.get('samples')} samples)"


def build_report() -> str:
    tasks = open_tasks()
    lines = [
        "PCI STATUS",
        "=" * 40,
        f"Branch:            {_git('rev-parse', '--abbrev-ref', 'HEAD') or 'unknown'}",
        f"Last commit:       {_git('log', '-1', '--format=%s') or 'unknown'}",
        f"Unsaved changes:   {len(_git('status', '--short').splitlines())} file(s)",
        f"Latest release:    {last_change()}",
        f"Quant verification: {last_verification()}",
        f"Open tasks:        {len(tasks)}",
    ]
    lines += [f"  next {i}: {t}" for i, t in enumerate(tasks[:3], 1)]
    lines += ["", "Commands: make check | make verify | make run | make help"]
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_report())
    sys.exit(0)
