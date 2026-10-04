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

The division name describes its intent: **XRPL : NFT Liquidity Ecosystem**. Detailed product definitions are not yet recorded in this repository. Items marked *to be defined* are intentionally left open so they can be filled in by the division owner, not guessed.

## What exists today

- **Code:** `backend/services/liquidity.py` (live pool depth for `PCI_XRPL_001`), `arcana_enterprise_nfts/mint.py`
- **API:** `GET /api/real_time_liquidity`, `GET /api/nft/collections`

## Product IDs

| Product ID | Definition |
|------------|-----------|
| `PCI_XRPL_001` | *To be defined* |
| `PCI_XRPL_002` | *To be defined* |
| `PCI_XRPL_003` | *To be defined* |

## Next steps

- Configure pool addresses for `PCI_XRPL_002` and `PCI_XRPL_003`.
- Record each product's definition in the table above, then update the registry if fields are added.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
