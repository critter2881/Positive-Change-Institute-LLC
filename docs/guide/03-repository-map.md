# Chapter 3 — A Map of the Repository

```
.
├── backend/                  Flask API (Chapter 6)
│   ├── app.py                Application factory and all routes
│   └── services/
│       ├── liquidity.py      On-chain pool depth with TTL cache
│       └── defi_analysis.py  DeFi architecture analysis
├── frontend/index.html       Static enterprise landing page
├── apo/apo.py                Aegis Prometheus Oracle server (Chapter 8)
├── arcana_enterprise_nfts/   NFT catalog and XRPL minting (Chapter 7)
├── config/                   Canonical JSON registries (Chapter 4)
├── auto_task_sync.py         Manifest → GitHub Issues sync (Chapter 9)
├── tests/test_backend.py     pytest suite
├── docs/                     Reference docs and this guide
├── reports/summary.json      Generated report output
├── tasks.md · CHANGELOG.md   Work tracking and history
└── .github/workflows/ci.yml  CI pipeline (Chapter 11)
```

## What runs, and where

| Component | Command | Port |
|-----------|---------|------|
| Backend API | `python backend/app.py` | 5000 (`FLASK_PORT`) |
| APO server | `python apo/apo.py` | 8000 |
| NFT minting | `python arcana_enterprise_nfts/mint.py` | n/a (XRPL) |
| Task sync | `python auto_task_sync.py` | n/a (GitHub API) |

## Dependencies between parts

```
config/*.json ──► backend/app.py ◄── arcana_enterprise_nfts/arcana_nfts.py
                       │
                       ├─► services/liquidity.py  ──► XRPL RPC / Jupiter API
                       ├─► services/defi_analysis.py
                       └─► OpenAI / Grok (optional, Prometheus)
apo/apo.py  (standalone, standard library only)
```

The backend imports the NFT catalog at startup. If the import fails it logs a warning and serves empty NFT endpoints rather than crashing. APO is standalone and imports nothing from the rest of the repo.

## Where to go next
[Chapter 4 — Configuration and Registries](04-configuration-and-registries.md)
