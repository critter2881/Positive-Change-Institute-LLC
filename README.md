# Positive Change Institute LLC

> **Where visionary strategy meets autonomous intelligence — shaping the future of digital ecosystems, one self-evolving innovation at a time.**

[![CI](https://github.com/critter2881/Positive-Change-Institute-LLC/actions/workflows/ci.yml/badge.svg)](https://github.com/critter2881/Positive-Change-Institute-LLC/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)

---

## Overview

Positive Change Institute LLC develops fully automated, AAA-grade turnkey digital solutions including XRPL and Solana token economies, NFT ecosystems with auto-evolving dynamics, and cross-platform dApps — all designed to transform digital ecosystems into living, scalable businesses.

Founded and led by **Christopher S. Rowland Sr.**, the Institute leverages proprietary AI pipelines combining GPT, Grok, and multi-intelligence architectures to orchestrate sophisticated, self-optimizing digital ecosystems.

---

## Quick Start

```bash
# Bootstrap
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Run backend
python backend/app.py

# Verify
curl http://127.0.0.1:5000/health
```

---

## Repository Structure

```
Positive-Change-Institute-LLC/
├── backend/                      # Flask REST API (app factory pattern)
│   └── app.py
├── frontend/                     # Static landing page
│   └── index.html
├── config/                       # Single-source-of-truth registries
│   ├── wallet_registry.json      # Canonical wallet definitions
│   └── divisions_registry.json   # Canonical division + product-ID map
├── arcana_enterprise_nfts/       # NFT collections and tier templates
├── tests/                        # pytest suite (24 tests)
│   └── test_backend.py
├── docs/                         # Project documentation
│   ├── API.md                    # REST API reference
│   ├── ARCHITECTURE.md           # Architecture overview
│   ├── SETUP.md                  # Setup and deployment guide
│   └── CONTRIBUTING.md           # Contribution guidelines
├── scripts/                      # Utility scripts
├── .github/workflows/            # GitHub Actions CI/CD
├── .env.example                  # Environment variable reference
├── requirements.txt              # Python dependencies
├── LICENSE
└── CHANGELOG.md
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness / readiness probe |
| `GET` | `/api/divisions` | All registered divisions and product IDs |
| `GET` | `/api/wallets` | Public wallet registry |
| `GET` | `/api/product_metadata` | Metadata for a wallet + product ID pair |
| `GET` | `/api/real_time_liquidity` | On-chain liquidity pool depths (XRPL, Solana) |
| `GET` | `/api/nft/collections` | Full Arcana Enterprise NFT catalog |
| `GET` | `/api/nft/collections/<id>` | Single NFT entry by product ID |
| `POST` | `/api/prometheus/execute` | Prometheus AI orchestration (GPT-4o / Grok-3) |
| `GET` | `/api/analytics/summary` | Aggregated dashboard summary |
| `GET` | `/api/gamification/tiers` | ArcanaPass tier definitions |
| `GET` | `/api/gamification/tiers/<name>` | Single gamification tier |
| `GET` | `/api/tokenomics/model` | Linear-vesting tokenomics projection |
| `GET` | `/api/compliance/check` | Wallet address format + risk check |

Full reference: [`docs/API.md`](docs/API.md)

---

## Enterprise Divisions (14)

Quantum AI · Arcane Blockchain · HyperSaaS · XRPL NFT Ecosystem · MID25 Tokenomics ·
MNR26 Reset Dashboard · ELF Meme Coin · CryptoArcana QSYS · Arcanex Optimizer ·
ArcanaPass · Prometheus Orchestrator · Foundry Analytics · Linktree Gateway · Corporate Modules

---

## Documentation

| Document | Purpose |
|----------|---------|
| [docs/API.md](docs/API.md) | REST API reference |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture overview |
| [docs/SETUP.md](docs/SETUP.md) | Setup and deployment |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Contribution guidelines |

---

## License

[MIT](LICENSE) © 2026 Positive Change Institute LLC
