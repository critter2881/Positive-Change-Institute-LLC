# Chapter 13 — Roadmap and Open Work

This chapter is the honest list of what is not finished. Sources are `tasks.md`, the registries, and gaps visible in the code.

## Declared initiatives (`tasks.md`)

| Initiative | Open items |
|------------|-----------|
| Prometheus AI | Architecture design, training data pipeline, deployment UI |
| Auto-Foundry Pipeline | CI/CD pipeline, testing integrations, performance monitoring |
| Midnight Relics NFT Collection | Specification and minting process, launch marketing, community plan |

## Gaps identified in the repository

1. **Divisions without implementations.** Most of the 16 registry entries have product IDs but no dedicated code (Chapter 5).
2. **Liquidity coverage.** Only `PCI_XRPL_001` has a configured pool, so everything else reports `no_pool_configured`.
3. **DeFi analysis uses sample inputs.** Wiring it to live pool data would make `/api/defi/analysis` operational.
4. ~~Task sync lacks de-duplication.~~ Done: `auto_task_sync.py` now skips titles that already have an open issue.
5. **Claims need evidence.** APO's headline figures need a measurement method or should stay labeled as claims.
6. **Single-branch hygiene.** Keep `main` canonical and archive stale branches and repositories (Chapter 2).

## How to propose work

Open an issue, link it to a division and product ID, and add a line to `tasks.md` once accepted. Close the loop in `CHANGELOG.md`.

## Where to go next
[Chapter 14 — Glossary](14-glossary.md)
