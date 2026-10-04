# APO : Aegis Prometheus Oracle : Sovereign Metadata

> Division 13 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_APO_001`, `PCI_APO_002`, `PCI_APO_003`, `PCI_APO_004`, `PCI_APO_005`, `PCI_APO_006`, `PCI_APO_007` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Implemented (descriptive)** |

## Purpose

Sovereign metadata oracle for multi-chain, multi-system integrity: one oracle, one law, one truth (from apo/apo.py META).

Product definitions below were **confirmed by the owner on 2026-10-04**. They derive from this description, the existing code, and the registry. Amend them here when they change.

## What exists today

- **Code:** `apo/apo.py` (standard-library server serving metadata, stats, whitepapers, docs)
- **API:** APO server on port 8000: `/api/apo_stats`, `/api/meta`, `/api/apo_whitepapers`, `/api/apo_docs`

## Product IDs

| Product ID | Definition |
|------------|-----------|
| `PCI_APO_001` | APO core whitepaper |
| `PCI_APO_002` | APO technical whitepaper |
| `PCI_APO_003` | APO operational whitepaper |
| `PCI_APO_004` | APO enterprise whitepaper |
| `PCI_APO_005` | APO doctrine whitepaper |
| `PCI_APO_006` | APO IP protection whitepaper |
| `PCI_APO_007` | APO value and pricing whitepaper |

## Next steps

- Map the seven `PCI_APO_*` IDs to the seven whitepapers; add evidence for headline figures.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
