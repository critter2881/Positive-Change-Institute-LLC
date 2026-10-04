# ArcanaPass : Tiered NFT Liquidity

> Division 11 of 16. Back to the [divisions index](README.md).

## Registry entry

| Field | Value |
|-------|-------|
| Product IDs | `PCI_ARP_001`, `PCI_ARP_002`, `PCI_ARP_003` |
| Chain | not set |
| Liquidity | No pool addresses configured; liquidity reports `no_pool_configured`. |
| Implementation status | **Partial** |

## Purpose

The division name describes its intent: **ArcanaPass : Tiered NFT Liquidity**. Detailed product definitions are not yet recorded in this repository. Items marked *to be defined* are intentionally left open so they can be filled in by the division owner, not guessed.

## What exists today

- **Code:** Gamification tiers in `backend/app.py`; NFT catalog in `arcana_enterprise_nfts/arcana_nfts.py`
- **API:** `GET /api/gamification/tiers`, `GET /api/gamification/tiers/<name>`, `GET /api/nft/collections/<product_id>`

## Product IDs

| Product ID | Definition |
|------------|-----------|
| `PCI_ARP_001` | *To be defined* |
| `PCI_ARP_002` | *To be defined* |
| `PCI_ARP_003` | *To be defined* |

## Next steps

- Define what each `PCI_ARP_*` product ID represents and map it to a tier.
- Record each product's definition in the table above, then update the registry if fields are added.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
