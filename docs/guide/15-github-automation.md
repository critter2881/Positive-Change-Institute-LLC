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
| Auto-update merge | `workflows/dependabot-auto-merge.yml` | Auto-merges Dependabot patch and minor updates once required checks pass. Major updates, and any PR labeled `hold`, wait for a human. | Dependabot PRs |
| Quant verification | `workflows/quant-verify.yml`, `scripts/quant_verify.py` | Checks model invariants (tokenomics, AMM, resilience, NFT evolution). The random seed **rotates weekly** and a failing seed can be replayed. | Weekly, on model changes, manual |
| Auto-assign | `workflows/auto-assign.yml`, `auto-assign.yml`, `CODEOWNERS` | Assigns each new issue and PR to the next worker in the pool (round-robin by number). CODEOWNERS adds the right reviewer by path. | Issue or PR opened |
| PR template | `pull_request_template.md` | Standard checklist on every PR | PR opened |

## Auto-evolution and auto-rotation

- **Auto-evolution:** `arcana_enterprise_nfts/evolution/engine.py` computes an NFT's level and traits from an activity score (thresholds 0, 100, 500). It is deterministic, and exposed at `GET /api/nft/collections/<product_id>/evolve?score=`.
- **Auto-rotation:** the quant check's seed changes every ISO week, so each scheduled run tests different inputs while staying reproducible (`--seed N`). Dependency updates rotate in daily through Dependabot.
- **"Quant verified" means** these invariants hold: circulating supply never exceeds supply, FDV is at least market cap, vesting is monotonic and ends at 100%, price impact is monotonic within [0, 1), the resilience score is within 0–100, and NFT evolution never regresses as the score rises. It is a self-consistency check of PCI's models, not an external audit or market validation.

## Assigning workers

Edit `.github/auto-assign.yml` and list GitHub usernames under `workers`. Only the owner is listed now, since collaborators are not known to this repository. Items that already have an assignee, and bot-authored items, are left alone. Assignees must have access to the repository, or GitHub ignores the assignment.

## Safeguards summary

- **Dependency auto-merge:** patch and minor only, never when labeled `hold`, and only after required checks pass.
- **Minting:** capped per run, mainnet needs two explicit confirmations (Chapter 7).
- **AI routing:** retries are bounded, failures degrade gracefully, and low-agreement cross-checks are flagged for review (Chapter 6).

## Safety notes

- Auto-merge needs "Allow auto-merge" enabled in repository settings, and branch protection with required checks. Without required checks, GitHub merges immediately.

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
