# Chapter 1 — Introduction: What This Guide Is

Positive Change Institute LLC (PCI) builds automated digital systems: token economies on XRPL and Solana, NFT ecosystems, AI orchestration, and enterprise tooling. Those systems live in one repository, and this guide explains all of it.

## How to read this guide

| If you are... | Start with |
|---------------|-----------|
| New to PCI | Chapters 1–3 |
| A developer | Chapters 4–9, then 11 |
| An operator or reviewer | Chapters 3, 10, 12 |
| Looking for a term | Chapter 14 (Glossary) |

Every chapter ends with a "Where to go next" pointer, so the book can be read straight through.

## The one-sentence model

> PCI is a set of **divisions**, each owning **product IDs**, served through one **API**, enriched by **Prometheus** (AI orchestration) and **APO** (metadata integrity), monetized through **Arcana NFTs** and **gamification tiers**, and governed by the **white paper**.

## Ground rules this guide follows

- **Code is the authority.** Where this guide and the code disagree, the code wins and the guide should be fixed. API behavior is verified against `backend/app.py` and `docs/API.md`.
- **Claims are labeled.** Figures such as APO's integrity percentages are *stated in the APO metadata*. This repository does not independently measure them.
- **No secrets.** Credentials are only ever read from environment variables. See Chapter 10.

## Where to go next
[Chapter 2 — The Mission and the Organization](02-mission-and-organization.md)
