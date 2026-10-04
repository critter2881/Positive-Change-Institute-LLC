# Chapter 15 — GitHub Automation

Automation that keeps this repository healthy without manual effort. Everything lives in `.github/`.

| Automation | File | What it does | Trigger |
|-----------|------|--------------|---------|
| CI | `workflows/ci.yml` | flake8, syntax check, pytest (3.11 and 3.12), config JSON validation | Push and PR to `main` |
| CodeQL | `workflows/codeql.yml` | Security analysis of the Python code | Push and PR to `main`, weekly |
| Dependabot | `dependabot.yml` | Opens PRs for outdated pip packages and GitHub Actions | Weekly |
| Auto-label | `workflows/labeler.yml`, `labeler.yml` | Labels PRs by the paths they touch | PR opened or updated |
| Stale cleanup | `workflows/stale.yml` | Marks items stale after 60 days and closes after 14 more. The `pinned` and `security` labels are exempt. | Daily |
| Release drafter | `workflows/release-drafter.yml`, `release-drafter.yml` | Drafts release notes from merged PRs, grouped by label | Push to `main` |
| Task sync | `auto_task_sync.py` | Creates GitHub Issues from a manifest, skipping duplicates | Manual run |
| NFT autogen, project board | `workflows/arcana_nft_autogen.yml`, `workflows/sync_to_project_board.yaml` | Existing workflows | See each file |
| PR template | `pull_request_template.md` | Standard checklist on every PR | PR opened |

## Safety notes

- The labeler uses `pull_request_target` but never checks out PR code, so untrusted code never runs with write access.
- All workflows declare least-privilege `permissions`.
- Pin or review third-party actions when you update them. Dependabot proposes the updates.

## One-time setup in GitHub settings (cannot be done from code)

1. Settings → Branches: protect `main`, require PRs, and require the CI jobs.
2. Settings → Code security: enable Dependabot alerts and secret scanning with push protection.
3. Create the labels used above (`backend`, `frontend`, `documentation`, `nft`, `prometheus-apo`, `config`, `automation`, `dependencies`, `pinned`, `security`).

## Across all of your repositories

These are repository-level files. To reuse them everywhere, create a public repository named `.github` under your account and put `ISSUE_TEMPLATE/`, `pull_request_template.md`, and workflow templates in it. Then copy `dependabot.yml`, `codeql.yml`, and `stale.yml` into each repository, or use GitHub's organization rulesets if you move the repositories to an organization.

## Where to go next
[Chapter 14 — Glossary](14-glossary.md)
