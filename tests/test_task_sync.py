"""Tests for auto_task_sync de-duplication."""

from unittest.mock import MagicMock, patch

import auto_task_sync as sync


def _resp(status, payload):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = payload
    return r


def test_issue_exists_true_for_matching_open_issue():
    with patch.object(sync.requests, "get", return_value=_resp(200, [{"title": "A"}])):
        assert sync.issue_exists("A", "o/r") is True


def test_issue_exists_ignores_pull_requests():
    payload = [{"title": "A", "pull_request": {}}]
    with patch.object(sync.requests, "get", return_value=_resp(200, payload)):
        assert sync.issue_exists("A", "o/r") is False


def test_issue_exists_returns_none_on_http_error():
    with patch.object(sync.requests, "get", return_value=_resp(500, [])):
        assert sync.issue_exists("A", "o/r") is None


def test_create_task_skips_duplicate():
    with patch.object(sync, "issue_exists", return_value=True), \
            patch.object(sync.requests, "post") as post:
        sync.create_task("A", "t", "o/r", {})
        post.assert_not_called()


def test_create_task_posts_when_new():
    with patch.object(sync, "issue_exists", return_value=False), \
            patch.object(sync.requests, "post", return_value=_resp(201, {})) as post:
        sync.create_task("A", "t", "o/r", {})
        post.assert_called_once()


def test_create_task_skips_when_issue_lookup_fails():
    with patch.object(sync, "issue_exists", return_value=None), \
            patch.object(sync.requests, "post") as post:
        sync.create_task("A", "t", "o/r", {})
        post.assert_not_called()
