# API Reference — Positive Change Institute LLC

Base URL (local development): `http://127.0.0.1:5000`

All responses are `application/json`. Non-`2xx` responses include an `error` key describing the problem.

---

## Health

### `GET /health`

Liveness and readiness probe. Use this endpoint in load-balancer health checks and Kubernetes probes.

**Response `200`**
```json
{
  "status": "ok",
  "service": "positive-change-institute"
}
```

---

## Divisions

### `GET /api/divisions`

Returns all registered enterprise divisions with their associated product IDs.

**Response `200`**
```json
[
  {
    "name": "Quantum AI : Market Liquidity Engine",
    "product_ids": ["PCI_AI_001", "PCI_AI_002", "PCI_AI_003"]
  },
  ...
]
```

---

## Wallets

### `GET /api/wallets`

Returns the public wallet registry.

**Response `200`**
```json
[
  {
    "label": "Base",
    "chain": "Base",
    "address": "geekstinkbreath.base.eth",
    "role": "operational"
  },
  ...
]
```

---

## Product Metadata

### `GET /api/product_metadata`

Resolves a wallet label and product ID to division metadata.

**Query parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `wallet` | yes | Wallet label (e.g. `Base`, `Xaman XRPL`) |
| `product_id` | yes | Product identifier (e.g. `PCI_AI_001`) |

**Response `200`**
```json
{
  "wallet": "Base",
  "wallet_address": "geekstinkbreath.base.eth",
  "product_id": "PCI_AI_001",
  "division": "Quantum AI : Market Liquidity Engine"
}
```

**Response `400`** — missing required parameters

```json
{ "error": "Missing required query parameters: 'wallet' and 'product_id'" }
```

**Response `404`** — unknown wallet or product ID

```json
{ "error": "Unknown wallet: 'INVALID'" }
```

---

## Real-Time Liquidity

### `GET /api/real_time_liquidity`

Returns on-chain liquidity pool depths for all divisions and product IDs. Data is fetched
live from chain RPC endpoints (XRPL, Solana) and cached for 60 seconds. Falls back to
stale cache or `"unavailable"` if the live fetch fails.

**Response `200`**
```json
{
  "XRPL : NFT Liquidity Ecosystem": {
    "PCI_XRPL_001": {
      "pool_depth": 2847.123456,
      "source": "live",
      "fetched_at": "2026-08-03T15:54:07Z"
    },
    "PCI_XRPL_002": {
      "pool_depth": null,
      "source": "no_pool_configured",
      "fetched_at": null
    }
  }
}
```

**`source` values:**

| Value | Meaning |
|-------|---------|
| `live` | Freshly fetched from chain |
| `cached` | Served from TTL cache (< 60 s old) |
| `stale_cache` | Live fetch failed; last known value returned |
| `no_pool_configured` | No pool address set for this product ID |
| `unavailable` | Fetch failed and no cache exists |

---

## DeFi Analysis

### `GET /api/defi/analysis`

Returns the default PCI DeFi architecture analysis snapshot spanning AMM, LP, yield,
lending, bridge, routing, scenario stress tests, and a composite resilience score.

**Response `200`**
```json
{
  "amm": {
    "curve": "xyk",
    "invariant": 400000000000.0,
    "fee": 0.003
  },
  "lp": {
    "impermanent_loss_estimate": 0.004,
    "fee_apr": 0.1,
    "volatility_exposure": "low"
  },
  "yield": {
    "real_yield": 0.05,
    "emissions": 0.02,
    "synthetic_yield": 0.01,
    "yield_quality": "high"
  },
  "lending": {
    "utilization": 0.375,
    "collateral_factor": 0.75,
    "liquidation_risk": "low",
    "oracle_risk": "low"
  },
  "bridge": {
    "finality_seconds": 180,
    "trust_model": "optimistic",
    "oracle_risk": "medium"
  },
  "routing": {
    "route_count": 2,
    "mev_exposure": "low",
    "solver_network": "supported"
  },
  "scenarios": {
    "volatility": {"shock": "volatility", "impact": "medium"},
    "liquidity": {"shock": "liquidity_withdrawal", "impact": "medium"},
    "oracle_failure": {"shock": "oracle_failure", "impact": "medium"},
    "governance_change": {"shock": "governance_change", "impact": "low"},
    "fee_shift": {"shock": "fee_shift", "impact": "medium"}
  },
  "resilience_score": 100
}
```

---

## NFT Collections

### `GET /api/nft/collections`

Returns the full Arcana Enterprise NFT catalog.

**Response `200`** — array of NFT entries with fields:
`collection`, `tier`, `product_id`, `one_time_price_usd`, `subscription_tiers`,
`auto_evolution`, `enterprise_utility`, `evolution_paths`, `storefront_link`.

### `GET /api/nft/collections/<product_id>`

Returns a single NFT entry by product ID (e.g. `FORGE-001`).

**Response `404`** — unknown product ID.

---

## Prometheus AI Orchestrator

### `POST /api/prometheus/execute`

Routes a task to the Prometheus AI intelligence layer. Uses OpenAI (`OPENAI_API_KEY`) or
Grok (`GROK_API_KEY`) if configured; otherwise falls back to a doctrine-based local router.

**Request body**
```json
{
  "task": "Analyze XRPL liquidity trends",
  "division": "XRPL : NFT Liquidity Ecosystem",
  "context": {}
}
```

**Response `200`**
```json
{
  "task": "Analyze XRPL liquidity trends",
  "division": "XRPL : NFT Liquidity Ecosystem",
  "routed_division": "XRPL : NFT Liquidity Ecosystem",
  "result": "AI-generated response …",
  "model": "gpt-4o",
  "status": "ok",
  "timestamp": "2026-08-03T15:54:07Z"
}
```

**Response `400`** — missing `task` field.

---

## Analytics

### `GET /api/analytics/summary`

Returns an aggregated dashboard summary.

**Response `200`**
```json
{
  "division_count": 14,
  "wallet_count": 5,
  "total_product_ids": 33,
  "nft_collection_count": 3,
  "gamification_tier_count": 3,
  "api_version": "2.0.0",
  "generated_at": "2026-08-03T15:54:07Z"
}
```

---

## Gamification

### `GET /api/gamification/tiers`

Returns ArcanaPass tier definitions with feature unlocks and pricing.

### `GET /api/gamification/tiers/<tier_name>`

Returns a single tier by name (case-insensitive). Valid values: `Adaptive`, `Mythic`, `Legendary`.

**Response `404`** — unknown tier; includes `valid_tiers` array.

---

## Tokenomics

### `GET /api/tokenomics/model`

Returns a linear-vesting tokenomics projection.

**Query parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `supply` | int | `1000000` | Total token supply |
| `initial_price` | float | `0.01` | USD price at TGE |
| `distribution` | float | `0.30` | Public allocation (0–1) |

**Response `200`**
```json
{
  "supply": 1000000,
  "initial_price_usd": 0.01,
  "public_distribution": 0.3,
  "circulating_supply": 300000,
  "market_cap_usd": 3000.0,
  "fully_diluted_valuation_usd": 10000.0,
  "liquidity_depth_estimate_usd": 300.0,
  "vesting_schedule": [
    {"month": 0, "circulating_pct": 0.3},
    {"month": 6, "circulating_pct": 0.45},
    {"month": 12, "circulating_pct": 0.6},
    {"month": 18, "circulating_pct": 0.75},
    {"month": 24, "circulating_pct": 1.0}
  ],
  "model": "linear_vesting"
}
```

**Response `400`** — invalid or out-of-range parameters.

---

## Compliance

### `GET /api/compliance/check`

Validates a wallet address format and returns a risk assessment.

**Query parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `address` | yes | Wallet address to check |
| `chain` | yes | Chain identifier (`XRPL`, `Solana`, `ETH`, `Base`, `Coinbase`) |

**Response `200`**
```json
{
  "address": "rhz5LkGZXz4fEs5T9neWtXC2vJpRVLoXVB",
  "chain": "XRPL",
  "format_valid": true,
  "risk_flags": [],
  "status": "clear",
  "checked_at": "2026-08-03T15:54:07Z"
}
```

**`status` values:** `clear` | `flagged` | `invalid_format`

**Response `400`** — missing required parameters.

---

## Error Format

All error responses share the same shape:

```json
{
  "error": "Human-readable error message",
  "detail": "Optional additional context"
}
```
