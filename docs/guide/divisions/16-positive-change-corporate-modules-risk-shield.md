# Positive Change : Corporate Modules : Risk & Shield

> Division 16 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_PCC_001`, `PCI_PCC_002`, `PCI_PCC_003` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Partial** |

## Purpose

Risk management and compliance modules ensuring institutional-grade protection across all operations.

Product definitions below were **confirmed by the owner on 2026-10-04**. They derive from this description, the existing code, and the registry. Amend them here when they change.

## What exists today

- **Code:** `_validate_address` in `backend/app.py`
- **API:** `GET /api/compliance/check`

## Product IDs

| Product ID | Definition |
|------------|-----------|
| `PCI_PCC_001` | Risk management module |
| `PCI_PCC_002` | Compliance screening (`/api/compliance/check`) |
| `PCI_PCC_003` | Institutional protection and audit controls |

## Next steps

- Define the three `PCI_PCC_*` products; extend beyond format and pattern screening.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
