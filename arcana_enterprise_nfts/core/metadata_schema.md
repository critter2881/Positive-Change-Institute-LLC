# Metadata Schema — Arcana Enterprise NFTs

This document defines the deterministic on-chain/off-chain metadata schema used across the Arcana Enterprise NFT System. The schema emphasizes reproducibility, auditability, and compliance-ready fields.

JSON Schema (example)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Arcana Enterprise NFT Metadata",
  "type": "object",
  "required": [
    "ticker",
    "classification",
    "version",
    "evolution_state",
    "audit_ref",
    "sovereign_watermark",
    "created_at"
  ],
  "properties": {
    "ticker": { "type": "string", "description": "Canonical short identifier for the NFT (e.g., ARC-FG-0001)" },
    "classification": { "type": "string", "enum": ["ULTRA-RARE","RARE","STANDARD"], "description": "Tier classification" },
    "version": { "type": "string", "description": "Semantic version of metadata schema (e.g., 1.0.0)" },
    "evolution_state": {
      "type": "object",
      "properties": {
        "level": { "type": "integer" },
        "last_event": { "type": "string" },
        "updated_at": { "type": "string", "format": "date-time" }
      },
      "required": ["level","updated_at"]
    },
    "audit_ref": { "type": "string", "description": "Immutable audit reference (hash or URI to audit record)" },
    "sovereign_watermark": { "type": "string", "description": "PCI sovereign watermark token (verifiable)" },
    "renderer_version": { "type": "string", "description": "Deterministic FX renderer version" },
    "checksum": { "type": "string", "description": "Content checksum (SHA-256) for reproducible rendering" },
    "license": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "issuer": { "type": "object", "properties": { "name": {"type":"string"}, "org_id": {"type":"string"} } },
    "signature": { "type": "string", "description": "Optional cryptographic signature over canonical fields" }
  }
}
```

Best practices
- Keep canonical fields (ticker, classification, version, checksum, audit_ref, sovereign_watermark) immutable whenever possible.
- Never rely on mutable presentation fields (images, thumbnails) for compliance checks — use checksum and renderer_version.
- Publish evolution events in the evolution audit log and reference the log entry hash in audit_ref.
- Sign canonical payloads with an issuer key; include signature for off-chain verification.

Files to add alongside this schema
- core/metadata_examples/*.json — real-world examples per tier
- core/validators/ — simple validation scripts (Node/Go/Python)

