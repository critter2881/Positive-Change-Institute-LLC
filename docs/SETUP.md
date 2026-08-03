# Setup & Deployment Guide

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.11 |
| pip | 23.x |
| Git | 2.x |

---

## Local Development

### 1 — Clone and bootstrap

```bash
git clone https://github.com/critter2881/Positive-Change-Institute-LLC.git
cd Positive-Change-Institute-LLC

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

### 2 — Start the backend

```bash
python backend/app.py
# Server listening on http://127.0.0.1:5000
```

Verify with:

```bash
curl http://127.0.0.1:5000/health
# {"service":"positive-change-institute","status":"ok"}
```

### 3 — Open the frontend

Open `frontend/index.html` in any modern browser. No build step required.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_HOST` | `127.0.0.1` | Host for the Flask server |
| `FLASK_PORT` | `5000` | Port for the Flask server |
| `FLASK_DEBUG` | `false` | Enable Flask debug mode |
| `LOG_LEVEL` | `INFO` | Python log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

Copy `.env.example` and adjust as needed. The `.env` file is excluded from version control.

---

## Running Tests

```bash
# All tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=backend --cov-report=term-missing -v
```

---

## Linting

```bash
python -m flake8 backend/ tests/ --max-line-length=100
```

---

## Production Deployment

> The backend is a standard WSGI Flask application. Deploy it with any production-grade WSGI server.

### Gunicorn (recommended)

```bash
pip install gunicorn
gunicorn "backend.app:create_app()" \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Environment hardening checklist

- [ ] Set `FLASK_DEBUG=false`
- [ ] Set `LOG_LEVEL=INFO` or `WARNING`
- [ ] Serve behind a reverse proxy (nginx, Caddy)
- [ ] Enable HTTPS / TLS termination at the proxy
- [ ] Pin dependency versions for reproducible builds

---

## CI/CD

GitHub Actions workflows are defined in `.github/workflows/`:

| Workflow | Trigger | Jobs |
|----------|---------|------|
| `ci.yml` | Push / PR to `main` | Lint → Syntax check → Tests (3.11 + 3.12) → Config validation |
| `arcana_nft_autogen.yml` | Push to `arcana_enterprise_nfts/` | Export NFT metadata to JSON |
| `sync_to_project_board.yaml` | Push / closed PR | Project board sync (placeholder) |
