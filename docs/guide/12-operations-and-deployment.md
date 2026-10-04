# Chapter 12 — Operations and Deployment

See [SETUP.md](../SETUP.md) for the full installation guide. This chapter covers running the system day to day.

## Components to operate

| Service | Entry point | Health signal |
|---------|-------------|---------------|
| Backend API | `backend/app.py` | `GET /health` returns `{"status":"ok"}` |
| APO | `apo/apo.py` | `GET /api/meta` returns `200` |
| Frontend | `frontend/index.html` | Static file served `200` |

## Configuration for production

- Set `FLASK_DEBUG=false` and bind deliberately with `FLASK_HOST`.
- Run the Flask app behind a production WSGI server and a reverse proxy. The built-in `app.run` is for development.
- Provide secrets (`OPENAI_API_KEY`, `GROK_API_KEY`) through your platform's secret store, not files in the repository.
- Point load-balancer and Kubernetes probes at `/health`.
- Set `LOG_LEVEL=INFO` (or `WARNING`) and ship logs to central storage.

## Behavior under failure

| Failure | Result |
|---------|--------|
| XRPL or Solana endpoint unreachable | Liquidity falls back to `stale_cache`, then `unavailable`. The API still returns `200`. |
| No AI key configured | Prometheus returns a `[DEMO]` response |
| NFT catalog import fails | Warning logged and NFT endpoints return empty lists |
| Unhandled exception | Generic `500` JSON and the stack trace is logged |

## Routine tasks

- **Weekly:** review CI status and dependency updates.
- **Per release:** run the Chapter 10 release checklist, update `CHANGELOG.md`, and tag the release.
- **Per registry change:** validate JSON and run tests.
- **Incident:** check `/health`, then logs, then the external dependency table above.

## Where to go next
[Chapter 13 — Roadmap and Open Work](13-roadmap.md)
