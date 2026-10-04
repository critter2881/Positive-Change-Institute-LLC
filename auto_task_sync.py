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


def _headers() -> dict:
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def issue_exists(title: str, repo: str) -> bool | None:
    """Return True if an open issue with exactly this title already exists.

    Return None when the lookup fails, so task creation can fail closed.
    """
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    page = 1
    try:
        while True:
            response = requests.get(
                url,
                headers=_headers(),
                params={"state": "open", "per_page": 100, "page": page},
                timeout=15,
            )
            if response.status_code != 200:
                logger.warning(
                    "Could not list issues in %s: HTTP %d", repo, response.status_code
                )
                return None
            issues = response.json()
            if not isinstance(issues, list):
                logger.warning("Could not list issues in %s: invalid response", repo)
                return None
            for issue in issues:
                if not isinstance(issue, dict):
                    logger.warning("Could not list issues in %s: invalid response", repo)
                    return None
                if "pull_request" not in issue and issue.get("title") == title:
                    return True
            if len(issues) < 100:
                return False
            page += 1
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Issue lookup failed for %s: %s", repo, exc)
        return None


def create_task(name: str, task_type: str, repo: str, stats: dict) -> None:
    """Create a GitHub Issue for the given project entry (skips duplicates)."""
    exists = issue_exists(name, repo)
    if exists is True:
        logger.info("Skipping '%s' in %s: open issue already exists", name, repo)
        return
    if exists is None:
        logger.error("Skipping '%s' in %s: issue lookup failed", name, repo)
        return
    url = f"{GITHUB_API_URL}/repos/{repo}/issues"
    headers = _headers()
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
        project_repo = project.get("repo", GITHUB_REPO)
        if project_repo != GITHUB_REPO:
            logger.warning(
                "Project '%s' targets a different repo ('%s'); "
                "expected '%s'. Verify this is intentional.",
                project.get("name", "Unnamed project"),
                project_repo,
                GITHUB_REPO,
            )
        create_task(
            name=project.get("name", "Unnamed project"),
            task_type=project.get("type", "unknown"),
            repo=project_repo,
            stats=project.get("stats", {}),
        )


if __name__ == "__main__":
    main()
