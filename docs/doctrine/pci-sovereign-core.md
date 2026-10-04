# PCI Sovereign Core

**Source:** [`critter2881/prometheus-pci-core-`](https://github.com/critter2881/prometheus-pci-core-) (Apache-2.0 there).

## Purpose

A Python engine intended to drive PCI's Whop storefront: product pages, pricing tiers, bundles, a UI layout model, and operator surfaces. Its README calls itself the canonical source for PCI product logic and pricing.

> **Status.** The source repository contains only a `README.md` and a `LICENSE`. The files the README describes (`pci_core.py`, `pci_api.py`, `requirements.txt`) are **not present** there, so this is a design specification, not working code.

## The golden-ratio model (φ ≈ 1.618)

| Element | Rule as specified |
|---------|-------------------|
| Tier price | `Price = Base × φⁿ`, where *n* is the tier level |
| Monthly price | `Monthly = Base / φ` |
| Tiers (low to high) | Micro-Access, Operator, Professional, Elite, Platform, Enterprise, Sovereign |
| Bundles | 2 products × 1.618, 3 products × 2.618, 5 products × 4.236 (Fibonacci-based multipliers) |

Illustration, for a base price of 10: tier prices run 10, 16.18, 26.18, 42.36, 68.54, 110.90, 179.44 (rounded).

## Seven-harmonic product hierarchy

1. φ¹ Prometheus Runtime Codex
2. φ² Omega Quant Authority
3. φ³ Prometheus Foundry
4. φ⁴ PCI Treasury Console
5. φ⁵ PCI Identity Matrix
6. φ⁶ PCI Visualization Suite
7. φ⁷ PCI Narrative Engine

## UI spiral model

Seven layers: core panel, secondary panels, context panels, telemetry clusters, harmonic overlays, identity geometry, narrative labels.

## Planned API

`GET /` status and product keys · `GET /storefront` full model · `GET /products` ordered list · `GET /product/{key}` one product. Planned dependencies: `fastapi`, `uvicorn`. Deploy targets named: Railway, Render, Fly.io, Azure, AWS, Vercel.

## Where it fits here

The pricing and tier ideas overlap with the [ArcanaPass tiers](../guide/07-arcana-nfts-and-arcanapass.md) and [value and pricing whitepaper](../guide/08-prometheus-and-apo.md). The two use different numbers today. Reconciling them is an open decision for the owner.

## Open items

- Decide whether to implement this engine in this repository (the φ-ladder is small and deterministic, so it would be straightforward to build and test) or keep it as design only.
- Confirm base prices before any implementation.
