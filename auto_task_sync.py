"""
auto_task_sync.py — Sync project tasks from Ultimate_Manifest.json to GitHub Issues.

Usage:
    GITHUB_TOKEN=<token> GITHUB_REPO=<owner/repo> python auto_task_sync.py

Environment variables:
    GITHUB_TOKEN   Personal access token with `repo` scope (required)
    GITHUB_REPO    Target repository in owner/repo format (required)
    MANIFEST_PATH  Path to the manifest JSON file (default: Ultimate_Manifest.json)
"""

import json
import logging
import os
import sys

import requests

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration — from environment variables only (no hardcoded secrets)
# ---------------------------------------------------------------------------
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")
MANIFEST_PATH = os.environ.get("MANIFEST_PATH", "Ultimate_Manifest.json")


def _validate_config() -> None:
    """Exit early with a clear message if required env vars are missing."""
    missing = [v for v in ("GITHUB_TOKEN", "GITHUB_REPO") if not os.environ.get(v)]
    if missing:
        logger.error(
            "Missing required environment variables: %s. "
            "Set them before running this script.",
            ", ".join(missing),
        )
        sys.exit(1)


def create_task(name: str, task_type: str, repo: str, stats: dict) -> None:
    """Create a GitHub Issue for the given project entry."""
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    stats_json = json.dumps(stats, indent=2)
    payload = {
        "title": name,
        "body": f"**Task Type:** {task_type}\n\n**Stats:**\n```json\n{stats_json}\n```",
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 201:
            logger.info("Created issue for '%s' in %s", name, repo)
        else:
            logger.error(
                "Failed to create issue for '%s' in %s: HTTP %d — %s",
                name,
                repo,
                response.status_code,
                response.text,
            )
    except requests.RequestException as exc:
        logger.error("Request error for '%s' in %s: %s", name, repo, exc)


def main() -> None:
    _validate_config()

    if not os.path.isfile(MANIFEST_PATH):
        logger.error("Manifest file not found: %s", MANIFEST_PATH)
        sys.exit(1)

    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        projects = json.load(fh)

    for project in projects:
        create_task(
            name=project.get("name", "Unnamed project"),
            task_type=project.get("type", "unknown"),
            repo=project.get("repo", GITHUB_REPO),
            stats=project.get("stats", {}),
        )


if __name__ == "__main__":
    main()
