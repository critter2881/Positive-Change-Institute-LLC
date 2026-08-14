# Changelog

All notable changes to this project are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [2.0.0] - 2026-08-03

### Added
- **Backend** — app factory pattern (`create_app()`) enabling clean testing and configurable startup.
- **Health endpoint** — `GET /health` for liveness/readiness probes.
- **`GET /api/divisions`** — returns all divisions and product IDs from the canonical registry.
- **`GET /api/wallets`** — returns the public wallet registry with chain and role metadata.
- **Proper error handling** — structured JSON error responses for `400`, `404`, and `500`.
- **Structured logging** — configurable log level via `LOG_LEVEL` environment variable.
- **Input validation** — `product_metadata` endpoint validates required parameters and returns `400`/`404` instead of silent fallbacks.
- **`config/divisions_registry.json`** — single authoritative source for all division and product-ID data.
- **`tests/test_backend.py`** — 24 pytest tests covering every endpoint, error case, and response shape.
- **`docs/API.md`** — complete REST API reference.
- **`docs/ARCHITECTURE.md`** — architecture overview and repository structure.
- **`docs/SETUP.md`** — local development and production deployment guide.
- **`docs/CONTRIBUTING.md`** — contribution workflow, branching, commit conventions, and PR checklist.
- **`.env.example`** — environment variable reference.
- **Frontend** — polished, responsive enterprise landing page with navigation, hero, stats strip, division cards, API reference section, and footer.
- **CI/CD** — enhanced GitHub Actions workflow with four jobs: `lint` (flake8), `syntax` (py_compile all files), `test` (pytest on Python 3.11 and 3.12 with coverage), and `validate-config` (JSON validation).

### Changed
- **`backend/app.py`** — refactored from procedural to app factory; registries now loaded from `config/` JSON files rather than hardcoded.
- **`README.md`** — rewritten as a professional, structured enterprise README with quick start, structure map, endpoint table, and doc links.
- **`.gitignore`** — expanded to cover pytest cache, coverage artefacts, IDE files, and log files.
- **`auto_task_sync.py`** — hardcoded GitHub token removed; all credentials now read exclusively from environment variables with clear error on missing config.
- **`requirements.txt`** — added `pytest`, `pytest-cov`, and `flake8` for CI.

### Removed
- **`config/wallets.json`** — duplicate of `config/wallet_registry.json`; removed to establish a single source of truth.
- **`test-workflow.md`** — placeholder file with no production value.

---

## [1.0.0] - 2026-08-03

### Added
- Initial Positive Change Institute filing-style structure.
- Wallet registry including Xaman XRPL.
- Division registry.
- Documentation outputs.
- Reports output.
- Canonical JSON records.

