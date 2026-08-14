"""
Positive Change Institute LLC
Enterprise Flask Backend — Application Factory
"""

import datetime
import json
import logging
import os
import re
import sys
from pathlib import Path

import requests
from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_BACKEND_DIR = Path(__file__).resolve().parent
_BASE_DIR = _BACKEND_DIR.parent
_CONFIG_DIR = _BASE_DIR / "config"


def _load_json(path: Path) -> dict:
    """Load a JSON file and return its contents."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _build_wallet_map(registry: dict) -> dict:
    """Flatten wallet_registry.json into {label: address} for quick lookup."""
    return {key: entry["address"] for key, entry in registry.items()}


def _build_divisions_map(registry: list) -> dict:
    """Convert divisions_registry.json list to {name: [product_ids]} dict."""
    return {entry["name"]: entry["product_ids"] for entry in registry}


# ---------------------------------------------------------------------------
# Module-level config constants
# ---------------------------------------------------------------------------
_GAMIFICATION_TIERS = [
    {
        "tier": "Adaptive",
        "collection": "Arcana Enterprise Forge\u00ae",
        "required_nft_product_id": "FORGE-001",
        "one_time_entry_usd": 999,
        "subscription_usd_month": 9,
        "api_rate_multiplier": 2,
        "feature_unlocks": [
            "advanced_analytics",
            "dashboard_integration",
            "workflow_automation",
            "priority_support",
        ],
    },
    {
        "tier": "Mythic",
        "collection": "Arcana Enterprise Relics\u00ae",
        "required_nft_product_id": "RELICS-001",
        "one_time_entry_usd": 4999,
        "subscription_usd_month": 199,
        "api_rate_multiplier": 5,
        "feature_unlocks": [
            "governance_voting",
            "automated_compliance",
            "corporate_rewards",
            "advanced_analytics",
            "priority_support",
        ],
    },
    {
        "tier": "Legendary",
        "collection": "Arcana Enterprise Ascendants\u00ae",
        "required_nft_product_id": "ASCEND-001",
        "one_time_entry_usd": 9999,
        "subscription_usd_month": 499,
        "api_rate_multiplier": 10,
        "feature_unlocks": [
            "all_features",
            "cross_chain_operations",
            "strategic_influence",
            "cinematic_integration",
            "governance_voting",
            "automated_compliance",
        ],
    },
]

# ---------------------------------------------------------------------------
# Address format validators (compliance)
# ---------------------------------------------------------------------------
_CHAIN_VALIDATORS: dict = {
    "XRPL": re.compile(r"^r[1-9A-HJ-NP-Za-km-z]{24,33}$"),
    "Solana": re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"),
    "ETH": re.compile(r"^0x[0-9a-fA-F]{40}$"),
    "Base": re.compile(r"^0x[0-9a-fA-F]{40}$"),
    "Coinbase": re.compile(r"^[0-9a-zA-Z._-]{3,30}$"),  # cb.id names
    "Multi-chain": None,  # accept any non-empty string
}

_RISK_PATTERNS = [
    ("all_zeros_eth", re.compile(r"^0x0{40}$")),
    ("burn_address", re.compile(r"^0xdead", re.IGNORECASE)),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validate_address(address: str, chain: str) -> tuple:
    """Return (format_valid: bool, risk_flags: list[str])."""
    validator = _CHAIN_VALIDATORS.get(chain)
    if validator is None:
        format_valid = bool(address)
    else:
        format_valid = bool(validator.match(address))

    risk_flags = [
        name for name, pattern in _RISK_PATTERNS if pattern.search(address)
    ]
    return format_valid, risk_flags


def _compute_tokenomics(
    supply: int, initial_price: float, distribution: float
) -> dict:
    """Return a linear-vesting tokenomics projection."""
    circulating = int(supply * distribution)
    market_cap = round(circulating * initial_price, 2)
    fdv = round(supply * initial_price, 2)
    liquidity_depth = round(market_cap * 0.10, 2)
    vesting = [
        {"month": 0, "circulating_pct": round(distribution, 4)},
        {"month": 6, "circulating_pct": round(min(distribution + 0.15, 1.0), 4)},
        {"month": 12, "circulating_pct": round(min(distribution + 0.30, 1.0), 4)},
        {"month": 18, "circulating_pct": round(min(distribution + 0.45, 1.0), 4)},
        {"month": 24, "circulating_pct": 1.0},
    ]
    return {
        "supply": supply,
        "initial_price_usd": initial_price,
        "public_distribution": distribution,
        "circulating_supply": circulating,
        "market_cap_usd": market_cap,
        "fully_diluted_valuation_usd": fdv,
        "liquidity_depth_estimate_usd": liquidity_depth,
        "vesting_schedule": vesting,
        "model": "linear_vesting",
    }


def _call_openai(
    task: str, division: str, context: dict, api_key: str, logger: logging.Logger
) -> tuple:
    """Call the OpenAI Chat Completions API. Returns (result_str, model_name)."""
    system = (
        "You are Prometheus, the AI orchestrator for Positive Change Institute LLC. "
        f"You are managing the '{division or 'all divisions'}' vertical. "
        "Respond with actionable intelligence in 1-3 concise sentences."
    )
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": task},
        ],
        "max_tokens": 256,
    }
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": "Bearer " + api_key},
            json=payload,
            timeout=20,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        return content, "gpt-4o"
    except Exception as exc:
        logger.error("OpenAI call failed: %s", exc)
        return "AI routing is temporarily unavailable.", "gpt-4o"


def _call_grok(
    task: str, division: str, context: dict, api_key: str, logger: logging.Logger
) -> tuple:
    """Call the Grok Chat API. Returns (result_str, model_name)."""
    system = (
        "You are Prometheus, the AI orchestrator for Positive Change Institute LLC. "
        f"You are managing the '{division or 'all divisions'}' vertical. "
        "Respond with actionable intelligence in 1-3 concise sentences."
    )
    payload = {
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": task},
        ],
        "max_tokens": 256,
    }
    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": "Bearer " + api_key},
            json=payload,
            timeout=20,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        return content, "grok-3"
    except Exception as exc:
        logger.error("Grok call failed: %s", exc)
        return "AI routing is temporarily unavailable.", "grok-3"


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
def create_app(config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    # Ensure project root is on sys.path so internal packages are importable
    # regardless of how the app is invoked (script vs. module).
    for _d in (str(_BASE_DIR), str(_BACKEND_DIR)):
        if _d not in sys.path:
            sys.path.insert(0, _d)

    from backend.services.defi_analysis import run_defi_analysis
    from backend.services.liquidity import get_all_liquidity

    app = Flask(__name__)

    # ---- Logging -----------------------------------------------------------
    log_level = (config or {}).get("LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO"))
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s \u2014 %(message)s",
    )
    logger = logging.getLogger(__name__)

    # ---- Load registries ---------------------------------------------------
    wallet_registry: dict = (config or {}).get(
        "WALLET_REGISTRY",
        _load_json(_CONFIG_DIR / "wallet_registry.json"),
    )
    divisions_registry: list = (config or {}).get(
        "DIVISIONS_REGISTRY",
        _load_json(_CONFIG_DIR / "divisions_registry.json"),
    )

    # ---- Load NFT catalog --------------------------------------------------
    nft_catalog: list = (config or {}).get("NFT_CATALOG")
    if nft_catalog is None:
        try:
            from arcana_enterprise_nfts.arcana_nfts import arcana_nfts
            nft_catalog = arcana_nfts
        except ImportError:
            logger.warning("arcana_nfts catalog not found; NFT endpoints will return []")
            nft_catalog = []

    # ---- Build lookup maps -------------------------------------------------
    WALLETS: dict = _build_wallet_map(wallet_registry)
    DIVISIONS: dict = _build_divisions_map(divisions_registry)

    logger.info(
        "Registries loaded \u2014 %d wallets, %d divisions, %d NFT entries",
        len(WALLETS),
        len(DIVISIONS),
        len(nft_catalog),
    )

    # ---- Error handlers ----------------------------------------------------
    @app.errorhandler(400)
    def bad_request(exc):
        return jsonify({"error": "Bad request", "detail": str(exc)}), 400

    @app.errorhandler(404)
    def not_found(exc):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(exc):
        logger.exception("Unhandled exception")
        return jsonify({"error": "Internal server error"}), 500

    # ========================================================================
    # Routes
    # ========================================================================

    # ---- Health ------------------------------------------------------------
    @app.route("/health", methods=["GET"])
    def health():
        """Liveness / readiness probe."""
        return jsonify({"status": "ok", "service": "positive-change-institute"}), 200

    # ---- Core registry endpoints -------------------------------------------
    @app.route("/api/divisions", methods=["GET"])
    def list_divisions():
        """Return all registered divisions with their product IDs."""
        return jsonify(
            [{"name": name, "product_ids": pids} for name, pids in DIVISIONS.items()]
        )

    @app.route("/api/wallets", methods=["GET"])
    def list_wallets():
        """Return the public wallet registry."""
        return jsonify(
            [
                {
                    "label": entry["label"],
                    "chain": entry["chain"],
                    "address": entry["address"],
                    "role": entry["role"],
                }
                for entry in wallet_registry.values()
            ]
        )

    @app.route("/api/product_metadata", methods=["GET"])
    def product_metadata():
        """Return metadata for a given wallet label and product ID."""
        wallet_label = request.args.get("wallet", "").strip()
        product_id = request.args.get("product_id", "").strip()

        if not wallet_label or not product_id:
            return (
                jsonify(
                    {
                        "error": (
                            "Missing required query parameters: "
                            "'wallet' and 'product_id'"
                        )
                    }
                ),
                400,
            )

        wallet_address = WALLETS.get(wallet_label)
        if wallet_address is None:
            return jsonify({"error": f"Unknown wallet: '{wallet_label}'"}), 404

        division = next(
            (name for name, pids in DIVISIONS.items() if product_id in pids),
            None,
        )
        if division is None:
            return jsonify({"error": f"Unknown product_id: '{product_id}'"}), 404

        return jsonify(
            {
                "wallet": wallet_label,
                "wallet_address": wallet_address,
                "product_id": product_id,
                "division": division,
            }
        )

    # ---- Real-time liquidity (on-chain service) ----------------------------
    @app.route("/api/real_time_liquidity", methods=["GET"])
    def real_time_liquidity():
        """Return on-chain liquidity pool depths per division and product ID."""
        return jsonify(get_all_liquidity(divisions_registry))

    @app.route("/api/defi/analysis", methods=["GET"])
    def defi_analysis():
        """Return the PCI sovereign DeFi architecture analysis snapshot."""
        return jsonify(run_defi_analysis())

    # ---- NFT Collections ---------------------------------------------------
    @app.route("/api/nft/collections", methods=["GET"])
    def nft_collections():
        """Return the full Arcana Enterprise NFT catalog."""
        return jsonify(nft_catalog)

    @app.route("/api/nft/collections/<product_id>", methods=["GET"])
    def nft_collection_detail(product_id: str):
        """Return a single NFT entry by product ID."""
        entry = next(
            (n for n in nft_catalog if n.get("product_id") == product_id), None
        )
        if entry is None:
            return jsonify({"error": f"Unknown NFT product_id: '{product_id}'"}), 404
        return jsonify(entry)

    # ---- Prometheus AI Orchestrator ----------------------------------------
    @app.route("/api/prometheus/execute", methods=["POST"])
    def prometheus_execute():
        """Route a task to the Prometheus AI intelligence layer."""
        body = request.get_json(silent=True) or {}
        task = body.get("task", "").strip()
        division = body.get("division", "").strip()
        context = body.get("context", {})

        if not task:
            return jsonify({"error": "Missing required field: 'task'"}), 400

        openai_key = os.getenv("OPENAI_API_KEY", "")
        grok_key = os.getenv("GROK_API_KEY", "")

        if openai_key:
            ai_result, model_used = _call_openai(
                task, division, context, openai_key, logger
            )
        elif grok_key:
            ai_result, model_used = _call_grok(
                task, division, context, grok_key, logger
            )
        else:
            ai_result = (
                f"[DEMO] Prometheus would route '{task}' for division "
                f"'{division or 'all'}' to the optimal intelligence layer. "
                "Set OPENAI_API_KEY or GROK_API_KEY to enable live AI routing."
            )
            model_used = "demo"

        return jsonify(
            {
                "task": task,
                "division": division or "all",
                "result": ai_result,
                "model": model_used,
                "status": "ok",
                "timestamp": _utcnow(),
            }
        )

    # ---- Analytics Dashboard -----------------------------------------------
    @app.route("/api/analytics/summary", methods=["GET"])
    def analytics_summary():
        """Return an aggregated summary across all divisions, products, and wallets."""
        total_products = sum(len(pids) for pids in DIVISIONS.values())
        return jsonify(
            {
                "division_count": len(DIVISIONS),
                "wallet_count": len(WALLETS),
                "total_product_ids": total_products,
                "nft_collection_count": len(nft_catalog),
                "gamification_tier_count": len(_GAMIFICATION_TIERS),
                "api_version": "2.0.0",
                "generated_at": _utcnow(),
            }
        )

    # ---- Gamification Tiers ------------------------------------------------
    @app.route("/api/gamification/tiers", methods=["GET"])
    def gamification_tiers():
        """Return ArcanaPass gamification tier definitions and feature unlocks."""
        return jsonify(_GAMIFICATION_TIERS)

    @app.route("/api/gamification/tiers/<tier_name>", methods=["GET"])
    def gamification_tier_detail(tier_name: str):
        """Return a specific gamification tier by name (case-insensitive)."""
        tier = next(
            (
                t
                for t in _GAMIFICATION_TIERS
                if t["tier"].lower() == tier_name.lower()
            ),
            None,
        )
        if tier is None:
            valid = [t["tier"] for t in _GAMIFICATION_TIERS]
            return (
                jsonify(
                    {"error": f"Unknown tier '{tier_name}'", "valid_tiers": valid}
                ),
                404,
            )
        return jsonify(tier)

    # ---- Tokenomics Model --------------------------------------------------
    @app.route("/api/tokenomics/model", methods=["GET"])
    def tokenomics_model():
        """Return a linear-vesting tokenomics model for given parameters.

        Query params:
          supply        (int,   default 1_000_000) — total token supply
          initial_price (float, default 0.01)      — USD price at TGE
          distribution  (float, default 0.30)      — public allocation (0–1)
        """
        try:
            supply = int(request.args.get("supply", 1_000_000))
            initial_price = float(request.args.get("initial_price", 0.01))
            distribution = float(request.args.get("distribution", 0.30))
        except (ValueError, TypeError):
            return (
                jsonify(
                    {
                        "error": (
                            "Invalid parameters: supply must be an integer, "
                            "initial_price and distribution must be floats"
                        )
                    }
                ),
                400,
            )

        if supply <= 0:
            return jsonify({"error": "supply must be a positive integer"}), 400
        if initial_price <= 0:
            return jsonify({"error": "initial_price must be a positive number"}), 400
        if not (0.0 < distribution <= 1.0):
            return (
                jsonify(
                    {
                        "error": (
                            "distribution must be greater than 0 and at most 1"
                        )
                    }
                ),
                400,
            )

        return jsonify(_compute_tokenomics(supply, initial_price, distribution))

    # ---- Compliance Check --------------------------------------------------
    @app.route("/api/compliance/check", methods=["GET"])
    def compliance_check():
        """Validate a wallet address format and return a risk assessment.

        Query params:
          address (str) — the wallet address to check
          chain   (str) — chain identifier (XRPL, Solana, ETH, Base, Coinbase, …)
        """
        address = request.args.get("address", "").strip()
        chain = request.args.get("chain", "").strip()

        if not address or not chain:
            return (
                jsonify(
                    {
                        "error": (
                            "Missing required query parameters: "
                            "'address' and 'chain'"
                        )
                    }
                ),
                400,
            )

        format_valid, risk_flags = _validate_address(address, chain)
        if risk_flags:
            status = "flagged"
        elif not format_valid:
            status = "invalid_format"
        else:
            status = "clear"

        return jsonify(
            {
                "address": address,
                "chain": chain,
                "format_valid": format_valid,
                "risk_flags": risk_flags,
                "status": status,
                "checked_at": _utcnow(),
            }
        )

    return app


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(
        host=os.getenv("FLASK_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
