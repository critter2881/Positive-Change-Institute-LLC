# Web3 Integration Examples — Ownership Detection & Gating

This file provides minimal, reproducible examples for Wallet Connect / QR-based gating and XRPL link handling.

Ownership detection (generic)
1. Client requests gated resource with wallet address (user connects wallet via WalletConnect/Web3Modal).
2. Server verifies ownership by querying chain indexer (e.g., TheGraph, Alchemy, XRPL ledger) for token ownership.
3. Server issues a short-lived JWT that encodes the NFT claim for the gated session.

Example: /api/gate/verify (pseudo)

Request:
POST /api/gate/verify
{
  "wallet_address": "0xabc...",
  "nft_ticker": "ARC-FG-0001"
}

Response (if owner):
{
  "ok": true,
  "jwt": "eyJhbGciOi...",
  "expires_at": "2026-06-22T09:00:00Z"
}

JWT claims to include
- sub: wallet address
- nft: ticker
- tier: ULTRA-RARE|RARE|STANDARD
- aud: your-service
- iat / exp
- proof: chain_event_reference (tx hash, block)

XRPL QR pattern
- QR should encode an XRPL payment or signed message request URI that the user approves in their XRPL wallet. For gating-only flows, prefer signed message verification over on-chain payments.

Security notes
- Use short JWT lifetimes for gating tokens and require re‑verification for sensitive actions.
- Rate limit /api/gate/verify and require captchas for anonymous requests.

