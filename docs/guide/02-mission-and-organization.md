# Chapter 2 — The Mission and the Organization

## Mission

PCI's tagline: *where visionary strategy meets autonomous intelligence, shaping the future of digital ecosystems, one self-evolving innovation at a time.* In practice that means:

1. **Automation first.** Workflows, minting, task sync, and analysis run from code.
2. **AI-assisted operation.** GPT, Grok, and a demo fallback are routed through the Prometheus layer.
3. **Auditability.** Every registry is a plain JSON file in source control.
4. **Compliance by design.** See Chapter 10 and the [White Paper](../WHITEPAPER.md).

Founder and leader: **Christopher S. Rowland Sr.** The full brand narrative is in [PCI_BRAND.md](../PCI_BRAND.md).

## Organizational structure

PCI is organized into **divisions** (16 entries in `config/divisions_registry.json`, the first being the Institute itself). Each division lists **product IDs** with the prefix `PCI_<DIVISION>_<NNN>`. Chapter 5 covers each one.

## The single source of truth principle

This repository is the system of record. The rules are:

- One canonical copy of each registry (`config/divisions_registry.json`, `config/wallet_registry.json`). Duplicates are removed. The changelog records `config/wallets.json` being deleted for this reason.
- Documentation lives under `docs/`; this guide lives under `docs/guide/`.
- Work in progress is tracked in `tasks.md`, and history in `CHANGELOG.md`.
- Placeholder or abandoned artifacts are removed or consolidated.

## Where to go next
[Chapter 3 — A Map of the Repository](03-repository-map.md)
