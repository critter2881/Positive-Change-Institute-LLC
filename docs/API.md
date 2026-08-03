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

Returns simulated real-time liquidity pool depths across all divisions and product IDs.

**Response `200`**
```json
{
  "Quantum AI : Market Liquidity Engine": {
    "PCI_AI_001": { "pool_depth": 284523.47 },
    "PCI_AI_002": { "pool_depth": 91230.18 },
    "PCI_AI_003": { "pool_depth": 432100.00 }
  },
  ...
}
```

> Note: `pool_depth` values are randomly generated on each request to simulate live data. A production implementation should integrate with on-chain data feeds.

---

## Error Format

All error responses share the same shape:

```json
{
  "error": "Human-readable error message",
  "detail": "Optional additional context"
}
```
