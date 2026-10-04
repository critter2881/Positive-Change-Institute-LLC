# Chapter 9 — Automation: Task Sync, Reports, and Frontend

## `auto_task_sync.py` — manifest to GitHub Issues

Reads a JSON manifest of projects and opens one GitHub Issue per project.

```bash
GITHUB_TOKEN=<token> GITHUB_REPO=<owner/repo> python auto_task_sync.py
```

| Variable | Required | Notes |
|----------|----------|-------|
| `GITHUB_TOKEN` | yes | Personal access token with `repo` scope |
| `GITHUB_REPO` | yes | `owner/repo` |
| `MANIFEST_PATH` | no | Defaults to `Ultimate_Manifest.json` |

Behavior worth knowing:

- Exits early with a clear message if required variables are missing, or if the manifest file is not found.
- Each manifest project provides `name`, `type`, optional `repo`, and `stats`. The issue body contains the task type and the stats as JSON.
- If a project's `repo` differs from `GITHUB_REPO`, it logs a **warning** before creating the issue. Check that this is intentional.
- Failures on one project are logged and do not stop the others.
- It does **not** de-duplicate. Running it twice creates duplicate issues.
- No token is hard-coded. A previous hard-coded token was removed (see the 2.0.0 changelog).

## `tasks.md`

A human-readable backlog grouped by initiative: Prometheus AI, Auto-Foundry Pipeline, and the Midnight Relics NFT Collection. It is the lightweight planning document; the roadmap is in Chapter 13.

## `reports/summary.json`

Generated report output kept under version control as a record.

## Frontend — `frontend/index.html`

A single static page: navigation, hero, stats strip, division cards, API reference section, and footer. It has no build step. Open it directly in a browser or serve it from any static host. Keep its division list consistent with `config/divisions_registry.json`.

## Where to go next
[Chapter 10 — Governance, Compliance, and Security](10-governance-compliance-security.md)
