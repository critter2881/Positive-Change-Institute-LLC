# Positive Change Institute LLC

> **Where visionary strategy meets autonomous intelligence — shaping the future of digital ecosystems, one self-evolving innovation at a time.**

[![CI](https://github.com/critter2881/Positive-Change-Institute-LLC/actions/workflows/ci.yml/badge.svg)](https://github.com/critter2881/Positive-Change-Institute-LLC/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License MIT](https://img.shields.io/badge/license-MIT-green)

---

## Overview

Positive Change Institute LLC develops fully automated, AAA-grade turnkey digital solutions including XRPL and Solana token economies, NFT ecosystems with auto-evolving dynamics, and cross-platform enterprise automation systems.

Founded and led by **Christopher S. Rowland Sr.**, the Institute leverages proprietary AI pipelines combining GPT, Grok, and multi-intelligence architectures to orchestrate sophisticated, self-optimizing workflows across product, operations, and compliance domains.

---

## Compliance and Governance Commitment

This repository is maintained with a strong commitment to professionalism, operational integrity, and compliance-aware engineering practices.

All products, services, workflows, and automation systems associated with this repository are intended to be developed, reviewed, and maintained in alignment with applicable legal, regulatory, contractual, and organizational requirements. This includes, where relevant, considerations related to the U.S. Clarity Act, enterprise governance, documentation standards, data handling, and system accountability.

### Principles
- Compliance considerations are treated as a design requirement, not an afterthought.
- Documentation should be clear, current, and suitable for long-term enterprise use.
- Automation should be auditable, maintainable, and operationally transparent.
- Source control should reflect a single coherent system of record.
- Placeholder, fragmentary, or abandoned artifacts should be removed or consolidated.

### Review Expectations
Before release or deployment, the repository and its outputs should be reviewed for:
- legal and policy alignment
- security and access control
- documentation completeness
- removal of empty or obsolete artifacts
- consistent structure across current and future automation workflows

### Status
This statement reflects the repository’s intended operating standard and governance posture. Final compliance determinations must be validated by qualified review against the specific requirements that apply to each use case.

---

## Clarity Act

This repository references the U.S. Clarity Act as part of its policy and documentation framework. Any enterprise automation, workflow organization, or compliance-related process in this repository should remain aligned with the Clarity Act where applicable.

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
├── tests/                        # pytest suite
│   ├── test_arcana_nfts.py
│   └── test_backend.py
├── docs/                         # Project documentation
│   ├── API.md                    # REST API reference
│   ├── ARCHITECTURE.md           # Architecture overview
│   ├── CONTRIBUTING.md           # Contribution guidelines
│   ├── PCI_BRAND.md              # Brand and identity reference
│   ├── README.md                 # Documentation index
│   └── SETUP.md                  # Setup and deployment guide
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
| `GET` | `/api/defi/analysis` | Sovereign DeFi architecture analysis snapshot |
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
| [docs/README.md](docs/README.md) | Top-level documentation overview |

---

## License

[MIT](LICENSE) © 2026 Positive Change Institute LLC
