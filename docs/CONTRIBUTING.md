# Contributing to Positive Change Institute LLC

Thank you for your interest in contributing. This guide explains how to work within the codebase and maintain the quality bar expected of this project.

---

## Code of Conduct

Be respectful, constructive, and professional in all interactions.

---

## Getting Started

1. Fork the repository and clone your fork.
2. Follow the [Setup Guide](SETUP.md) to bootstrap your local environment.
3. Create a feature branch from `main`:

```bash
git checkout -b feat/your-feature-name
```

---

## Branching Strategy

| Branch pattern | Purpose |
|----------------|---------|
| `main` | Production-ready code; protected |
| `feat/<name>` | New features |
| `fix/<name>` | Bug fixes |
| `chore/<name>` | Maintenance, dependency updates |
| `docs/<name>` | Documentation-only changes |

---

## Commit Messages

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body]
```

Common types: `feat`, `fix`, `chore`, `docs`, `test`, `refactor`, `ci`.

Examples:
- `feat(backend): add /api/divisions endpoint`
- `fix(config): correct Phantom chain label`
- `docs(api): document 404 error responses`

---

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] All tests pass: `python -m pytest tests/ -v`
- [ ] Lint is clean: `python -m flake8 backend/ tests/ --max-line-length=100`
- [ ] New behaviour is covered by tests
- [ ] Documentation is updated if the public API or config schema changed
- [ ] No secrets or credentials are included in the diff
- [ ] The PR description summarises what changed and why

---

## Adding a New Division or Wallet

1. **Divisions** — add a new entry to `config/divisions_registry.json`. Do not duplicate this data in `backend/app.py`; the backend loads the registry at startup.

2. **Wallets** — add a new entry to `config/wallet_registry.json`. The `config/wallets.json` file has been removed; `wallet_registry.json` is the single source of truth.

---

## Testing

- Tests live in `tests/`.
- Use `pytest` fixtures and the Flask test client; no real network calls.
- Group tests by endpoint in classes (`TestHealth`, `TestDivisions`, etc.).
- Aim for 100% branch coverage of `backend/app.py`.

---

## Reporting Issues

Open a GitHub Issue with:
- A clear title
- Steps to reproduce
- Expected vs. actual behaviour
- Environment details (OS, Python version)
