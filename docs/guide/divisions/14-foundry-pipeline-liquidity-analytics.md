# Foundry : Pipeline : Liquidity Analytics

> Division 14 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_FND_001`, `PCI_FND_002`, `PCI_FND_003` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Partial** |

## Purpose

Enterprise data pipeline and analytics suite delivering real-time liquidity visibility and forecasting.

Product definitions below are **proposed**: they are derived from this description, the existing code, and the registry, and are pending confirmation by the division owner.

## What exists today

- **Code:** `.github/workflows/ci.yml`, `auto_task_sync.py`
- **API:** None (tooling)

## Product IDs

| Product ID | Proposed definition |
|------------|-----------|
| `PCI_FND_001` | Enterprise data pipeline |
| `PCI_FND_002` | Real-time liquidity analytics dashboard (`/api/real_time_liquidity`) |
| `PCI_FND_003` | Liquidity forecasting |

## Next steps

- See the Auto-Foundry Pipeline items in `tasks.md`.
- Owner to confirm or amend the proposed product definitions above.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
