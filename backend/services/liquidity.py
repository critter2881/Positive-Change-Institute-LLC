"""
Liquidity service — fetches on-chain pool depths with in-memory TTL cache.

Supported chains
----------------
XRPL   — queries the public Ripple JSON-RPC HTTP endpoint (no key required).
Solana — queries the Jupiter Aggregator v2 price API (no key required).

For product IDs without a configured pool_address the record is returned with
source="no_pool_configured" and pool_depth=None so the API never errors.
"""

from __future__ import annotations

import datetime
import logging
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Network constants
# ---------------------------------------------------------------------------
_XRPL_RPC = "https://s1.ripple.com:51234"
_JUPITER_PRICE = "https://api.jup.ag/price/v2"
_REQUEST_TIMEOUT = 8  # seconds

# ---------------------------------------------------------------------------
# TTL cache
# ---------------------------------------------------------------------------
_CACHE_TTL = 60  # seconds


class _TTLCache:
    """Simple in-memory key→value store with per-entry TTL."""

    def __init__(self, ttl: int = _CACHE_TTL) -> None:
        self._ttl = ttl
        self._data: dict[str, tuple[float, dict]] = {}

    def get(self, key: str) -> Optional[dict]:
        """Return the cached value if still fresh, else None."""
        entry = self._data.get(key)
        if entry and (time.monotonic() - entry[0]) < self._ttl:
            return entry[1]
        return None

    def set(self, key: str, value: dict) -> None:
        self._data[key] = (time.monotonic(), value)

    def get_stale(self, key: str) -> Optional[dict]:
        """Return the last cached value regardless of TTL (fallback on failure)."""
        entry = self._data.get(key)
        return entry[1] if entry else None

    def clear(self) -> None:
        self._data.clear()


_cache = _TTLCache()


# ---------------------------------------------------------------------------
# Chain-specific fetchers
# ---------------------------------------------------------------------------
def _fetch_xrpl(pool_address: str) -> Optional[float]:
    """Return XRP balance (drops → XRP) for the given XRPL account address."""
    payload = {
        "method": "account_info",
        "params": [{"account": pool_address, "ledger_index": "validated"}],
    }
    try:
        resp = requests.post(_XRPL_RPC, json=payload, timeout=_REQUEST_TIMEOUT)
        resp.raise_for_status()
        balance_drops = (
            resp.json()
            .get("result", {})
            .get("account_data", {})
            .get("Balance")
        )
        if balance_drops is not None:
            return round(int(balance_drops) / 1_000_000, 6)  # drops → XRP
    except Exception as exc:
        logger.warning("XRPL fetch failed for %s: %s", pool_address, exc)
    return None


def _fetch_solana(pool_address: str) -> Optional[float]:
    """Return USD price for the given Solana mint address via Jupiter Aggregator."""
    try:
        resp = requests.get(
            _JUPITER_PRICE,
            params={"ids": pool_address},
            timeout=_REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        price_info = resp.json().get("data", {}).get(pool_address, {})
        price = price_info.get("price")
        if price is not None:
            return round(float(price), 6)
    except Exception as exc:
        logger.warning("Solana/Jupiter fetch failed for %s: %s", pool_address, exc)
    return None


_FETCHERS: dict = {
    "XRPL": _fetch_xrpl,
    "Solana": _fetch_solana,
}


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------
def fetch_product_liquidity(
    product_id: str, pool_address: str, chain: str
) -> dict:
    """
    Return a liquidity record for a single product.

    Result shape::

        {
            "pool_depth": float | None,
            "source": "live" | "cached" | "stale_cache"
                     | "no_pool_configured" | "unavailable",
            "fetched_at": "YYYY-MM-DDTHH:MM:SSZ" | None,
        }
    """
    if not pool_address:
        return {
            "pool_depth": None,
            "source": "no_pool_configured",
            "fetched_at": None,
        }

    cache_key = f"{chain}:{pool_address}"

    # --- Fresh cache hit ---
    fresh = _cache.get(cache_key)
    if fresh:
        return fresh

    # --- Live fetch ---
    fetcher = _FETCHERS.get(chain)
    if fetcher:
        depth = fetcher(pool_address)
        if depth is not None:
            record: dict = {
                "pool_depth": depth,
                "source": "live",
                "fetched_at": _utcnow(),
            }
            _cache.set(cache_key, record)
            return record

    # --- Stale cache fallback ---
    stale = _cache.get_stale(cache_key)
    if stale:
        logger.info("Returning stale cache for %s (%s)", product_id, cache_key)
        return {**stale, "source": "stale_cache"}

    return {"pool_depth": None, "source": "unavailable", "fetched_at": None}


def get_all_liquidity(divisions_registry: list) -> dict:
    """
    Return ``{division_name: {product_id: liquidity_record}}`` for all divisions.

    Each division entry may optionally include:
    - ``"chain"``: the primary chain identifier ("XRPL", "Solana", …)
    - ``"pool_addresses"``: ``{product_id: address}`` mapping
    """
    result: dict = {}
    for division in divisions_registry:
        name = division.get("name", "unknown")
        chain = division.get("chain", "")
        pool_addresses: dict = division.get("pool_addresses", {})
        result[name] = {
            pid: fetch_product_liquidity(
                pid, pool_addresses.get(pid, ""), chain
            )
            for pid in division.get("product_ids", [])
        }
    return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
