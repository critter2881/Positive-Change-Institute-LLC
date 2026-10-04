# XRPL : NFT Liquidity Ecosystem

> Division 5 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_XRPL_001`, `PCI_XRPL_002`, `PCI_XRPL_003` |
| Chain | XRPL |
| Liquidity | Pool addresses configured: `PCI_XRPL_001` |
| Implementation status | **Partial** |

## Purpose

XRP Ledger-native NFT collections with programmable royalties and auto-evolving metadata.

Product definitions below were **confirmed by the owner on 2026-10-04**. They derive from this description, the existing code, and the registry. Amend them here when they change.

## What exists today

- **Code:** `backend/services/liquidity.py` (live pool depth for `PCI_XRPL_001`), `arcana_enterprise_nfts/mint.py`
- **API:** `GET /api/real_time_liquidity`, `GET /api/nft/collections`

## Product IDs

| Product ID | Definition |
|------------|-----------|
| `PCI_XRPL_001` | Arcana Enterprise Forge® (Adaptive) NFT collection and its live liquidity pool (`FORGE-001`) |
| `PCI_XRPL_002` | Arcana Enterprise Relics® (Mythic) NFT collection (`RELICS-001`) |
| `PCI_XRPL_003` | Arcana Enterprise Ascendants® (Legendary) NFT collection (`ASCEND-001`) |

## Next steps

- Configure pool addresses for `PCI_XRPL_002` and `PCI_XRPL_003`.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
