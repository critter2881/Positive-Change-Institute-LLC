# Prometheus : AI Liquidity Orchestrator

> Division 12 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_PROM_001`, `PCI_PROM_002` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Partial** |

## Purpose

Superintelligence-powered orchestration layer coordinating cross-division liquidity flows in real time.

Product definitions below are **proposed**: they are derived from this description, the existing code, and the registry, and are pending confirmation by the division owner.

## What exists today

- **Code:** `/api/prometheus/execute` in `backend/app.py` (OpenAI, Grok, demo mode)
- **API:** `POST /api/prometheus/execute`

## Product IDs

| Product ID | Proposed definition |
|------------|-----------|
| `PCI_PROM_001` | Prometheus task router (`/api/prometheus/execute`: OpenAI, Grok, or demo mode) |
| `PCI_PROM_002` | Cross-division liquidity flow coordinator |

## Next steps

- Define the two product IDs; see the Prometheus AI items in `tasks.md`.
- Owner to confirm or amend the proposed product definitions above.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
