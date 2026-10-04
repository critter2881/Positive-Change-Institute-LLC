# Chapter 8 — Prometheus and the Aegis Prometheus Oracle (APO)

Two names appear throughout PCI materials. They are related but distinct:

- **Prometheus** is the *intelligence layer*: AI orchestration that routes tasks to a model. In code it is `POST /api/prometheus/execute` (Chapter 6). The wider doctrine calls it "Prometheus Superintelligence".
- **APO (Aegis Prometheus Oracle)** is the *integrity layer*: a metadata authority whose motto is "one oracle, one law, one truth". In code it is `apo/apo.py`.

## Running APO

```bash
python apo/apo.py        # http://127.0.0.1:8000
```

APO uses only the Python standard library (`http.server`). The server binds to `0.0.0.0:8000`, so restrict network exposure appropriately.

| Path | Returns |
|------|---------|
| `/` | Generated HTML app |
| `/api/apo_stats` | Headline stat cards |
| `/api/meta` | Who/what/when/where/why/how block |
| `/api/apo_whitepapers` | The whitepaper set |
| `/api/apo_docs` | Documentation and guidance |

Unknown paths return `404`; handler exceptions return `500`.

## The META block

APO describes itself through six questions:

| Question | Summary |
|----------|---------|
| Who | Owner PCI; product "Aegis Prometheus Oracle" |
| What | Sovereign metadata oracle; single source of truth for metadata integrity |
| When | Inception 2026; always-on |
| Where | Chains, metagraphs, sovereign stacks, enterprise systems |
| Why | Eliminate drift, manipulation, and corruption in metadata |
| How | Doctrine-locked rulesets, validator mesh, redundancy, Prometheus intelligence |

## The whitepaper set

`APO_WHITEPAPERS` contains seven documents: **core**, **technical**, **operational**, **enterprise**, **doctrine**, **ip**, and **value_pricing**. The `ip` paper sets trademark rules: first mention carries ™, marks are never altered, and the PCI copyright block appears on all documents. The `value_pricing` paper lists value claims and price points.

## About the numbers

APO's stat cards (for example, "99.997% metadata integrity", "12-layer doctrine", "14,000+ validator reach points") are **declarations in APO's own metadata**. This repository contains the descriptive content and server only; it does not include a validator network or a measurement harness. Treat these figures as product positioning until independently evidenced, and keep that distinction in any external communication (see Chapter 10).

## Where to go next
[Chapter 9 — Automation: Task Sync, Reports, and Frontend](09-automation-and-frontend.md)
