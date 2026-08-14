#!/usr/bin/env python3
"""
Arcana Enterprise NFT Minting Script
=====================================
Mints Arcana Enterprise NFT collections on the XRP Ledger using xrpl-py.

Usage
-----
Testnet (default — safe for testing, no real XRP spent)::

    XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py

Mint a specific NFT only::

    XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py --product-id FORGE-001

Mainnet (CAUTION — uses real XRP)::

    XRPL_WALLET_SEED=<seed> python arcana_enterprise_nfts/mint.py --mainnet

Environment variables
---------------------
XRPL_WALLET_SEED   XRPL wallet seed (required — NEVER commit this value)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path setup — ensure project root is importable as a package
# ---------------------------------------------------------------------------
_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from arcana_enterprise_nfts.arcana_nfts import arcana_nfts as NFT_CATALOG  # noqa: E402

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Network constants
# ---------------------------------------------------------------------------
_TESTNET_URL = "https://s.altnet.rippletest.net:51234"
_MAINNET_URL = "https://s1.ripple.com:51234"
_METADATA_BASE_URL = "https://enterprise.arcana.com/metadata"

# NFTokenMint flag: tfTransferable (token may be transferred to 3rd parties)
_FLAG_TRANSFERABLE = 8

# Transfer fee in basis points: 500 = 5 %  (max 50000 = 50 %)
_TRANSFER_FEE_BPS = 500


# ---------------------------------------------------------------------------
# Minting helpers
# ---------------------------------------------------------------------------
def _metadata_uri_hex(product_id: str) -> str:
    """Return a hex-encoded metadata URI for a given product ID."""
    from xrpl.utils import str_to_hex

    uri = f"{_METADATA_BASE_URL}/{product_id}.json"
    return str_to_hex(uri)


def _memo_hex(data: str) -> str:
    from xrpl.utils import str_to_hex

    return str_to_hex(data)


def mint_single(wallet, client, nft_data: dict) -> dict:
    """
    Mint a single NFTokenMint transaction for *nft_data* and return the result.

    Raises on failure so the caller can decide whether to continue or abort.
    """
    from xrpl.models.transactions import NFTokenMint
    from xrpl.transaction import submit_and_wait

    product_id = nft_data["product_id"]
    memo_payload = json.dumps(
        {
            "collection": nft_data["collection"],
            "tier": nft_data["tier"],
            "product_id": product_id,
            "copyright": nft_data.get("copyright_trademark", ""),
        },
        separators=(",", ":"),
    )

    txn = NFTokenMint(
        account=wallet.classic_address,
        nftoken_taxon=0,
        flags=_FLAG_TRANSFERABLE,
        transfer_fee=_TRANSFER_FEE_BPS,
        uri=_metadata_uri_hex(product_id),
        memos=[
            {
                "memo": {
                    "memo_data": _memo_hex(memo_payload),
                    "memo_type": _memo_hex("application/json"),
                }
            }
        ],
    )

    result = submit_and_wait(txn, client, wallet)
    return result.result


def mint_catalog(
    seed: str, network_url: str, product_id: str | None = None
) -> None:
    """
    Mint the entire NFT catalog (or a single entry) on the given XRPL network.
    """
    from xrpl.clients import JsonRpcClient
    from xrpl.wallet import Wallet

    targets = (
        [n for n in NFT_CATALOG if n["product_id"] == product_id]
        if product_id
        else list(NFT_CATALOG)
    )

    if not targets:
        logger.error("No NFT found with product_id=%r", product_id)
        sys.exit(1)

    client = JsonRpcClient(network_url)
    wallet = Wallet.from_seed(seed)
    logger.info("Connected to %s | Wallet: %s", network_url, wallet.classic_address)

    successes, failures = 0, 0
    for nft_data in targets:
        logger.info(
            "Minting '%s' (tier: %s, product_id: %s) …",
            nft_data["collection"],
            nft_data["tier"],
            nft_data["product_id"],
        )
        try:
            result = mint_single(wallet, client, nft_data)
            tx_result = result.get("meta", {}).get("TransactionResult", "unknown")
            if tx_result == "tesSUCCESS":
                logger.info("  \u2713 Minted — tx hash: %s", result.get("hash", "n/a"))
                successes += 1
            else:
                logger.error("  \u2717 Failed — TransactionResult: %s", tx_result)
                failures += 1
        except Exception as exc:
            logger.exception(
                "  \u2717 Exception minting %s: %s", nft_data["product_id"], exc
            )
            failures += 1

    logger.info(
        "Done — %d minted successfully, %d failed.", successes, failures
    )
    if failures:
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mint Arcana Enterprise NFTs on the XRP Ledger"
    )
    parser.add_argument(
        "--mainnet",
        action="store_true",
        help="Target XRPL mainnet. Default is testnet (altnet). "
        "CAUTION: mainnet transactions spend real XRP.",
    )
    parser.add_argument(
        "--product-id",
        metavar="ID",
        help="Mint a single NFT by product ID (e.g. FORGE-001). "
        "Omit to mint the entire catalog.",
    )
    args = parser.parse_args()

    seed = os.environ.get("XRPL_WALLET_SEED", "").strip()
    if not seed:
        logger.error(
            "XRPL_WALLET_SEED environment variable is required. "
            "Export it before running this script — never hard-code it."
        )
        sys.exit(1)

    network_url = _MAINNET_URL if args.mainnet else _TESTNET_URL
    network_label = "MAINNET \u26a0\ufe0f" if args.mainnet else "TESTNET"
    logger.info("Network: %s (%s)", network_label, network_url)

    mint_catalog(seed, network_url, product_id=args.product_id)


if __name__ == "__main__":
    main()
