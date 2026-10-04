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

Membership-gated NFT passes unlocking tiered liquidity rewards and enterprise governance rights.

Product definitions below are **proposed**: they are derived from this description, the existing code, and the registry, and are pending confirmation by the division owner.

## What exists today

- **Code:** Gamification tiers in `backend/app.py`; NFT catalog in `arcana_enterprise_nfts/arcana_nfts.py`
- **API:** `GET /api/gamification/tiers`, `GET /api/gamification/tiers/<name>`, `GET /api/nft/collections/<product_id>`

## Product IDs

| Product ID | Proposed definition |
|------------|-----------|
| `PCI_ARP_001` | Adaptive tier pass (Forge, `FORGE-001`) |
| `PCI_ARP_002` | Mythic tier pass (Relics, `RELICS-001`) |
| `PCI_ARP_003` | Legendary tier pass (Ascendants, `ASCEND-001`) |

## Next steps

- Define what each `PCI_ARP_*` product ID represents and map it to a tier.
- Owner to confirm or amend the proposed product definitions above.

## Related
[Enterprise Divisions overview](../05-enterprise-divisions.md) · [Backend API](../06-backend-api.md) · [Roadmap](../13-roadmap.md)
