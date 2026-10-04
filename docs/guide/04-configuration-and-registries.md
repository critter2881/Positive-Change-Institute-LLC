# Chapter 4 — Configuration and Registries

## Divisions registry — `config/divisions_registry.json`

A JSON list. Each entry has:

| Field | Required | Meaning |
|-------|----------|---------|
| `name` | yes | Division display name |
| `product_ids` | yes | List of `PCI_*` product identifiers |
| `chain` | no | Chain the division's pools live on (e.g. `XRPL`) |
| `pool_addresses` | no | Map of product ID → on-chain pool address |

Only entries with a `chain` and a `pool_addresses` mapping are queried for live liquidity (Chapter 6).

## Wallet registry — `config/wallet_registry.json`

A JSON object keyed by wallet label (for example `Base`, `Coinbase`, `Phantom`, `Xaman XRPL`). Each wallet has `label`, `chain`, `address`, and `role`. These are **public** identifiers only. Never put seeds or private keys here.

The `/api/product_metadata` endpoint joins a wallet label and a product ID to return division metadata.

## Environment variables — `.env.example`

Copy to `.env` and fill in. `.env` is git-ignored.

| Variable | Used by | Purpose |
|----------|---------|---------|
| `FLASK_HOST` / `FLASK_PORT` / `FLASK_DEBUG` | backend | Server binding and debug mode |
| `LOG_LEVEL` | backend | `DEBUG`…`CRITICAL` |
| `OPENAI_API_KEY` | Prometheus | Enables live GPT routing |
| `GROK_API_KEY` | Prometheus | Enables live Grok routing (used if no OpenAI key) |
| `XRPL_WALLET_SEED` | minting | Wallet seed. **Never commit.** |
| `GITHUB_TOKEN` / `GITHUB_REPO` / `MANIFEST_PATH` | task sync | See Chapter 9 |

## Changing a registry safely

1. Edit the JSON file.
2. Validate it: `python -c "import json,sys; json.load(open('config/divisions_registry.json'))"`. CI also does this.
3. Run `python -m pytest tests/ -v`.
4. Update [API.md](../API.md) if response shapes change, and add a `CHANGELOG.md` entry.

## Where to go next
[Chapter 5 — The Enterprise Divisions](05-enterprise-divisions.md)
