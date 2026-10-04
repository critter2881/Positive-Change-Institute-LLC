# Chapter 6 — The Backend API

The backend is a Flask application built by the factory `create_app(config=None)` in `backend/app.py`. The full request and response reference is [API.md](../API.md). This chapter explains *how it works and why*.

## Startup sequence

1. Add the project root to `sys.path` so internal packages import however the app is launched.
2. Configure logging from `LOG_LEVEL`.
3. Load `wallet_registry.json` and `divisions_registry.json` (or take them from the `config` argument, which is how tests inject data).
4. Load the NFT catalog, falling back to `[]` if the import fails.
5. Build lookup maps and register error handlers and routes.

Passing a `config` dict (`WALLET_REGISTRY`, `DIVISIONS_REGISTRY`, `NFT_CATALOG`, `LOG_LEVEL`) is the supported way to run isolated instances.

## Endpoint catalog

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness and readiness probe |
| GET | `/api/divisions` | All divisions and product IDs |
| GET | `/api/wallets` | Public wallet registry |
| GET | `/api/product_metadata?wallet=&product_id=` | Join wallet and product to division |
| GET | `/api/real_time_liquidity` | On-chain pool depths |
| GET | `/api/defi/analysis` | DeFi architecture analysis |
| GET | `/api/nft/collections` | Arcana NFT catalog |
| GET | `/api/nft/collections/<product_id>` | One NFT entry |
| POST | `/api/prometheus/execute` | AI task routing |
| GET | `/api/analytics/summary` | Aggregate counts |
| GET | `/api/gamification/tiers[/<name>]` | ArcanaPass tiers |
| GET | `/api/tokenomics/model` | Vesting projection |
| GET | `/api/compliance/check?address=&chain=` | Address format and risk check |

## Error contract

Every non-2xx response is JSON with an `error` key. `400`, `404`, and `500` have global handlers; `500` logs the stack trace server-side and returns a generic message, so internals are never leaked.

## Prometheus orchestration

`POST /api/prometheus/execute` accepts `{"task": "...", "division": "...", "context": {}}`.

- `task` is required, otherwise `400`.
- If `OPENAI_API_KEY` is set, the task goes to OpenAI.
- Otherwise, if `GROK_API_KEY` is set, it goes to Grok.
- Otherwise the endpoint runs in **demo mode** and returns a `[DEMO]` message with `model: "demo"`. This makes local development and tests free of external calls.

The response always includes `task`, `division` (defaulting to `all`), `result`, `model`, `status`, and `timestamp`.

## Liquidity service

`services/liquidity.py` returns `{division: {product_id: record}}`. The record's `source` field says how trustworthy the number is:

| `source` | Meaning |
|----------|---------|
| `live` | Fetched just now |
| `cached` | Fresh cache hit (TTL 60 seconds) |
| `stale_cache` | Live fetch failed, serving last known value |
| `no_pool_configured` | No pool address in the registry. `pool_depth` is `null`. |
| `unavailable` | No live data and nothing cached |

XRPL is queried through the public Ripple JSON-RPC endpoint and Solana through the Jupiter price API. Neither needs a key, and requests time out after 8 seconds. The API **never errors** because a pool is missing or a network is down. It degrades through the sources above.

Today only `PCI_XRPL_001` has a configured pool.

## DeFi analysis service

`services/defi_analysis.py` is a deterministic model with fixed sample inputs: a constant-product AMM (`x·y = k`) with price impact, LP impermanent-loss estimates, yield quality (real yield vs. emissions), lending utilization and liquidation risk, bridge trust, route and MEV exposure, five stress scenarios (volatility, liquidity, oracle failure, governance change, fee shift), and a capped 0–100 **resilience score**. It is an *analysis framework*, not live market data.

## Tokenomics model

`GET /api/tokenomics/model?supply=&initial_price=&distribution=` (defaults 1,000,000 / 0.01 / 0.30):

- circulating = supply × distribution
- market cap = circulating × price; FDV = supply × price
- liquidity depth estimate = 10% of market cap
- vesting: distribution at month 0, +15 percentage points per 6 months, full by month 24

Invalid input returns `400` with a specific message.

## Compliance check

Validates address format per chain (XRPL, Solana, ETH, Base, Coinbase, Multi-chain) and flags risk patterns (all-zeros and `0xdead…` burn addresses). `status` is `flagged`, `invalid_format`, or `clear`. This is a **format and pattern screen**, not sanctions screening or legal advice.

## Where to go next
[Chapter 7 — Arcana NFTs and ArcanaPass](07-arcana-nfts-and-arcanapass.md)
