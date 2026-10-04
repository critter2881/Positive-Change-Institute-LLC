# Chapter 5 — The Enterprise Divisions

The registry defines 16 entries. Product IDs below come directly from `config/divisions_registry.json`.

| # | Division | Product IDs | Theme |
|---|----------|-------------|-------|
| 1 | Positive Change Institute LLC | `PCI_ORG_001`–`003` | The parent organization |
| 2 | Quantum AI : Market Liquidity Engine | `PCI_AI_001`–`003` | AI-driven market liquidity |
| 3 | Arcane Blockchain : Token Liquidity Layer | `PCI_BC_001`–`002` | Token liquidity infrastructure |
| 4 | HyperSaaS : Gamified Liquidity Platforms | `PCI_SAAS_001`–`002` | Gamified SaaS |
| 5 | XRPL : NFT Liquidity Ecosystem | `PCI_XRPL_001`–`003` | NFTs on XRP Ledger (has a configured pool) |
| 6 | MID25 : Tokenomics Suite | `PCI_MID25_001`–`002` | Token modeling |
| 7 | MNR26 : Reset Dashboard | `PCI_MNR26_001`–`003` | Reset dashboard with gamification |
| 8 | ELF : Meme Coin | `PCI_ELF_001`–`003` | Viral liquidity |
| 9 | CryptoArcana : QSYS Liquidity Nodes | `PCI_QSYS_001`–`002` | Liquidity nodes |
| 10 | Arcanex : Stake & Liquidity Optimizer | `PCI_ARX_001`–`002` | Staking optimization |
| 11 | ArcanaPass : Tiered NFT Liquidity | `PCI_ARP_001`–`003` | Tiered access (Chapter 7) |
| 12 | Prometheus : AI Liquidity Orchestrator | `PCI_PROM_001`–`002` | AI orchestration (Chapter 6) |
| 13 | APO : Aegis Prometheus Oracle | `PCI_APO_001`–`007` | Metadata oracle (Chapter 8) |
| 14 | Foundry : Pipeline | `PCI_FND_001`–`003` | Pipeline analytics |
| 15 | Linktree : Liquidity Gateway | `PCI_LT_001`–`002` | Public gateway |
| 16 | Positive Change : Corporate Modules | `PCI_PCC_001`–`003` | Risk and shield |

> The README's "14 divisions" shorthand groups the marketing-level divisions. The registry file is authoritative.

## Division-to-code mapping

| Division | Where it is implemented today |
|----------|-------------------------------|
| XRPL NFT Ecosystem | `services/liquidity.py` (pool depth), `mint.py` |
| ArcanaPass | `/api/gamification/tiers` |
| MID25 tokenomics | `/api/tokenomics/model` |
| Prometheus | `/api/prometheus/execute` |
| APO | `apo/apo.py` |
| Quantum AI / Arcane Blockchain | `/api/defi/analysis` (DeFi analysis) |
| Corporate Modules (risk) | `/api/compliance/check` |
| Others | Registered in the registry. No dedicated code yet. |

The last row matters: some divisions are **registered and tracked**, but their products are not yet built. The roadmap in Chapter 13 treats this as the main growth area.

## Where to go next
[Chapter 6 — The Backend API](06-backend-api.md)
