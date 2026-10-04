# The Positive Change Institute Guide

A guide to everything in this repository, arranged to be read from start to finish.
Each part builds on the one before it, but any chapter can also be read on its own.

## Part I — Who We Are
1. [Brand & Mission](PCI_BRAND.md): what PCI is and why it exists.
2. [Repository Overview](../README.md): the Institute at a glance and where everything lives.

## Part II — How We Govern
3. [White Paper](WHITEPAPER.md): governance, compliance doctrine, and operating posture.
4. [Contributing](CONTRIBUTING.md): the quality bar and how to work within it.

## Part III — How It Is Built
5. [Architecture](ARCHITECTURE.md): system design and the source-of-truth map.
6. [API Reference](API.md): the REST endpoints the backend exposes.
7. [Setup & Deployment](SETUP.md): install, run, test, and deploy.

## Part IV — What We Offer
8. [Arcana Enterprise NFTs](../arcana_enterprise_nfts/README.md): the NFT system and its evolution protocols.
9. Enterprise divisions: see [`config/divisions_registry.json`](../config/divisions_registry.json) and the [README](../README.md#enterprise-divisions-14).
10. Prometheus automation: [`apo/`](../apo/) and [`auto_task_sync.py`](../auto_task_sync.py).

## Part V — What Is Happening Now
11. [Tasks](../tasks.md): current work.
12. [Changelog](../CHANGELOG.md): what has changed and when.

## Notes
- Preserve existing subdirectory systems unless explicitly updated later.
- Keep the top-level structure clean and GitHub-ready.
- Flask is required for the backend.
- API documentation should remain aligned with implemented backend routes.
