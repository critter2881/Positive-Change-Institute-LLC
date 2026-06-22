# Evolution Engine — Design & Audit Spec

This file specifies the Auto‑Evolution Engine behavior, event sources, state model, and the audit log format required for compliance.

Principles
- Deterministic: given the same event history and engine version, evolution must produce the same resulting state.
- Auditable: every change is recorded in an append‑only audit log with cryptographic anchors.
- Explainable: evolution rules must be human‑readable and versioned.

Event sources
- Mission completion events (signed by backend)
- Performance metrics (streaks, scores)
- Administrative adjustments (rare; requires multi‑sig)
- External recalibration (AI rarity recalibration runs)

State model (simplified)
- evolution.level: integer (0..N)
- evolution.branch: string (path of mutation)
- evolution.last_event_id: string (audit log id)
- evolution.renderer_profile: string

Rule examples
- On mission_complete with difficulty >= X and score >= Y -> level += 1
- On consistency_streak >= 7 days -> level += floor(streak_days / 7)
- On AI_rarity_recalibration -> recompute level based on scoring function (vX)

Audit log format (immutable JSON Lines — each line a single JSON object)

Example entry

```json
{
  "id": "evt_20260622_0001",
  "timestamp": "2026-06-22T08:00:00Z",
  "nft_ticker": "ARC-FG-0001",
  "engine_version": "evolution-v1.2.0",
  "event_type": "mission_complete",
  "event_source": "missions-service",
  "event_payload": { "mission_id": "msn_42", "difficulty": 5, "score": 890 },
  "delta": { "level_change": 1 },
  "resulting_state_hash": "sha256:...",
  "audit_ref": "ipfs://bafy...",
  "signature": "sig_kx..."
}
```

Compliance requirements
- Store audit logs in append‑only object storage (IPFS/AR/immutable S3 + ledger reference).
- Include resulting_state_hash that can be recomputed by validators using the canonical state format.
- Expose read endpoints for auditors: /audit/nft/{ticker}/events?from=&to=

Operational notes
- Keep evolution engine deterministic: freeze random seeds in engine releases and include seed in audit entries.
- Version rules and store them under evolution/rules/vN/*.yaml for reproducibility.

