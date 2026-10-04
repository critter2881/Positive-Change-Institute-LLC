# MID25 : Tokenomics Suite

> Division 6 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_MID25_001`, `PCI_MID25_002` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Partial** |

## Purpose

Precision tokenomics design, modeling, and deployment tooling for enterprise token launches.

Product definitions below are **proposed**: they are derived from this description, the existing code, and the registry, and are pending confirmation by the division owner.

## What exists today

- **Code:** `_compute_tokenomics` in `backend/app.py`
- **API:** `GET /api/tokenomics/model`

## Product IDs

| Product ID | Proposed definition |
|------------|-----------|
| `PCI_MID25_001` | Tokenomics design and modeling (`/api/tokenomics/model`) |
| `PCI_MID25_002` | Token launch deployment tooling |

## Next steps

- Define `PCI_MID25_001` and `PCI_MID25_002` and add scenario modeling beyond linear vesting.
- Owner to confirm or amend the proposed product definitions above.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
