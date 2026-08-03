"""
Positive Change Institute LLC
Enterprise Flask Backend — Application Factory
"""

import json
import logging
import os
import random
from pathlib import Path

from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent.parent
_CONFIG_DIR = _BASE_DIR / "config"


def _load_json(path: Path) -> dict:
    """Load a JSON file and return its contents."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _build_wallet_map(registry: dict) -> dict:
    """Flatten wallet_registry.json into {label: address} for quick lookup."""
    return {key: entry["address"] for key, entry in registry.items()}


def _build_divisions_map(registry: dict) -> dict:
    """Convert divisions_registry.json list to {name: [product_ids]} dict."""
    return {entry["name"]: entry["product_ids"] for entry in registry}


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
def create_app(config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # ---- Logging -----------------------------------------------------------
    log_level = (config or {}).get("LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO"))
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    )
    logger = logging.getLogger(__name__)

    # ---- Load registries from single authoritative sources -----------------
    wallet_registry: dict = (config or {}).get(
        "WALLET_REGISTRY",
        _load_json(_CONFIG_DIR / "wallet_registry.json"),
    )
    divisions_registry: list = (config or {}).get(
        "DIVISIONS_REGISTRY",
        _load_json(_CONFIG_DIR / "divisions_registry.json"),
    )

    WALLETS: dict = _build_wallet_map(wallet_registry)
    DIVISIONS: dict = _build_divisions_map(divisions_registry)

    logger.info(
        "Registries loaded — %d wallets, %d divisions",
        len(WALLETS),
        len(DIVISIONS),
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

    # ---- Routes ------------------------------------------------------------
    @app.route("/health", methods=["GET"])
    def health():
        """Liveness / readiness probe."""
        return jsonify({"status": "ok", "service": "positive-change-institute"}), 200

    @app.route("/api/divisions", methods=["GET"])
    def list_divisions():
        """Return all registered divisions with their product IDs."""
        return jsonify(
            [
                {"name": name, "product_ids": pids}
                for name, pids in DIVISIONS.items()
            ]
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
                    {"error": "Missing required query parameters: 'wallet' and 'product_id'"}
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

    @app.route("/api/real_time_liquidity", methods=["GET"])
    def real_time_liquidity():
        """Return simulated real-time liquidity pool depths per division."""
        data = {
            name: {
                pid: {"pool_depth": round(random.uniform(5_000, 500_000), 2)}
                for pid in pids
            }
            for name, pids in DIVISIONS.items()
        }
        return jsonify(data)

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
