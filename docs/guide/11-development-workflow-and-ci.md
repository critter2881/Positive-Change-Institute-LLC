# Chapter 11 — Development Workflow, Testing, and CI

The detailed rules are in [CONTRIBUTING.md](../CONTRIBUTING.md) and [SETUP.md](../SETUP.md). This is the short, ordered path.

## The loop

1. **Branch** from `main` using `feat/`, `fix/`, `chore/`, or `docs/` prefixes.
2. **Set up** with a virtualenv and `pip install -r requirements.txt`, then copy `.env.example` to `.env`.
3. **Change** code, tests, and docs together.
4. **Validate locally** (below).
5. **Commit** using Conventional Commits.
6. **Open a pull request** and complete the checklist in CONTRIBUTING.
7. **Record** user-visible changes in `CHANGELOG.md` (Keep a Changelog format).

## Local validation

```bash
python -m flake8 backend/ tests/ auto_task_sync.py --max-line-length=100
python -m pytest tests/ -v
```

Tests live in `tests/test_backend.py` and cover every endpoint, error case, and response shape. Because the app is a factory, tests build isolated instances with injected registries, and Prometheus runs in demo mode with no external calls.

## Continuous integration

`.github/workflows/ci.yml` runs four jobs on every change:

| Job | What it checks |
|-----|---------------|
| Lint (flake8) | Style and static errors |
| Syntax check | All Python files compile |
| Backend tests (pytest) | Test suite on Python 3.11 and 3.12 with coverage |
| Validate config JSON | Registry files are valid JSON |

A change is not ready until all four are green.

## Recipes

**Add an endpoint:** add the route in `create_app()`, add tests for success and every error path, document it in `docs/API.md`, then add a changelog entry.

**Add a division:** append to `divisions_registry.json` with unique `PCI_*` product IDs, validate the JSON, update Chapter 5 and the README counts, then run the tests.

**Add an NFT tier:** add the catalog entry, add the matching gamification tier in `app.py`, and keep `product_id` identical in both places.

## Where to go next
[Chapter 12 — Operations and Deployment](12-operations-and-deployment.md)
