# Chapter 7 — Arcana NFTs and ArcanaPass

Arcana Enterprise NFTs are PCI's access and identity layer. Each collection is a tier of utility, and the catalog and the tiers are linked by `product_id`. See also the [collection README](../../arcana_enterprise_nfts/README.md).

## The three collections

| Collection | Tier | Product ID | Entry price (USD) | Monthly (USD) | API rate multiplier |
|-----------|------|-----------|-------------------|---------------|---------------------|
| Arcana Enterprise Forge® | Adaptive | `FORGE-001` | 999 | 9 | 2× |
| Arcana Enterprise Relics® | Mythic | `RELICS-001` | 4,999 | 199 | 5× |
| Arcana Enterprise Ascendants® | Legendary | `ASCEND-001` | 9,999 | 499 | 10× |

Tier data is served by `/api/gamification/tiers`. The catalog is served by `/api/nft/collections`.

## Feature unlocks

- **Adaptive:** advanced analytics, dashboard integration, workflow automation, priority support.
- **Mythic:** governance voting, automated compliance, corporate rewards, advanced analytics, priority support.
- **Legendary:** all features, cross-chain operations, strategic influence, cinematic integration, governance voting, automated compliance.

## Anatomy of a catalog entry (`arcana_nfts.py`)

`collection`, `tier`, `product_id`, pricing and subscription fields, `auto_evolution`, `ai_powered`, `enterprise_utility`, `story_integration`, `rarity`, `diversification`, `motif`, `evolution_paths` (levels with trait lists), QR and wallet links, storefront link, and a copyright line.

**Evolution** means each NFT has levels (1–3 for Forge). Each level adds traits (for example, "Neon accent rings" at level 2, "Dynamic AI pattern overlay" at level 3).

## Minting on XRPL — `mint.py`

```bash
# Testnet (default, no real XRP)
XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py

# One NFT only
XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py --product-id FORGE-001

# Mainnet. Uses real XRP, so use with extreme care.
XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py --mainnet
```

Each mint is an XRPL `NFTokenMint` with taxon `0`, the *transferable* flag, a **5% transfer fee** (500 basis points), a metadata URI derived from the product ID, and a JSON memo (collection, tier, product ID, copyright).

### Minting safety rules
1. The seed comes from `XRPL_WALLET_SEED` only and is never committed or logged.
2. Always rehearse on testnet first.
3. Mainnet requires the explicit `--mainnet` flag.
4. Review `--product-id` targeting before a catalog-wide mint, since mints are not reversible.

## Where to go next
[Chapter 8 — Prometheus and the Aegis Prometheus Oracle (APO)](08-prometheus-and-apo.md)
