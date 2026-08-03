"""
Pytest test suite for the Positive Change Institute backend.

Runs against an in-memory Flask test client so no external services are needed.
"""

import json
import pytest

# ---------------------------------------------------------------------------
# App fixture — inject test registries so tests are hermetic
# ---------------------------------------------------------------------------
WALLET_REGISTRY = {
    "Base": {
        "label": "Base",
        "chain": "Base",
        "address": "geekstinkbreath.base.eth",
        "role": "operational",
    },
    "Xaman XRPL": {
        "label": "Xaman XRPL",
        "chain": "XRPL",
        "address": "rhz5LkGZXz4fEs5T9neWtXC2vJpRVLoXVB",
        "role": "operational",
    },
}

DIVISIONS_REGISTRY = [
    {
        "name": "Quantum AI : Market Liquidity Engine",
        "product_ids": ["PCI_AI_001", "PCI_AI_002"],
    },
    {
        "name": "XRPL : NFT Liquidity Ecosystem",
        "product_ids": ["PCI_XRPL_001"],
    },
]


@pytest.fixture()
def app():
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from backend.app import create_app

    flask_app = create_app(
        {
            "WALLET_REGISTRY": WALLET_REGISTRY,
            "DIVISIONS_REGISTRY": DIVISIONS_REGISTRY,
        }
    )
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
class TestHealth:
    def test_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_body_contains_ok_status(self, client):
        data = resp_json(client.get("/health"))
        assert data["status"] == "ok"

    def test_body_contains_service_name(self, client):
        data = resp_json(client.get("/health"))
        assert "service" in data


# ---------------------------------------------------------------------------
# GET /api/divisions
# ---------------------------------------------------------------------------
class TestDivisions:
    def test_returns_200(self, client):
        assert client.get("/api/divisions").status_code == 200

    def test_returns_list(self, client):
        data = resp_json(client.get("/api/divisions"))
        assert isinstance(data, list)

    def test_each_division_has_name_and_product_ids(self, client):
        data = resp_json(client.get("/api/divisions"))
        for item in data:
            assert "name" in item
            assert "product_ids" in item

    def test_known_division_present(self, client):
        data = resp_json(client.get("/api/divisions"))
        names = [d["name"] for d in data]
        assert "Quantum AI : Market Liquidity Engine" in names


# ---------------------------------------------------------------------------
# GET /api/wallets
# ---------------------------------------------------------------------------
class TestWallets:
    def test_returns_200(self, client):
        assert client.get("/api/wallets").status_code == 200

    def test_returns_list(self, client):
        data = resp_json(client.get("/api/wallets"))
        assert isinstance(data, list)

    def test_each_wallet_has_required_fields(self, client):
        data = resp_json(client.get("/api/wallets"))
        for w in data:
            for field in ("label", "chain", "address", "role"):
                assert field in w, f"Missing field '{field}' in wallet {w}"

    def test_known_wallet_present(self, client):
        data = resp_json(client.get("/api/wallets"))
        labels = [w["label"] for w in data]
        assert "Base" in labels


# ---------------------------------------------------------------------------
# GET /api/product_metadata
# ---------------------------------------------------------------------------
class TestProductMetadata:
    def test_valid_request_returns_200(self, client):
        resp = client.get(
            "/api/product_metadata?wallet=Base&product_id=PCI_AI_001"
        )
        assert resp.status_code == 200

    def test_valid_response_shape(self, client):
        data = resp_json(
            client.get("/api/product_metadata?wallet=Base&product_id=PCI_AI_001")
        )
        assert data["wallet"] == "Base"
        assert data["product_id"] == "PCI_AI_001"
        assert "division" in data
        assert "wallet_address" in data

    def test_correct_division_resolved(self, client):
        data = resp_json(
            client.get("/api/product_metadata?wallet=Base&product_id=PCI_AI_001")
        )
        assert data["division"] == "Quantum AI : Market Liquidity Engine"

    def test_missing_params_returns_400(self, client):
        assert client.get("/api/product_metadata").status_code == 400

    def test_missing_product_id_returns_400(self, client):
        assert client.get("/api/product_metadata?wallet=Base").status_code == 400

    def test_unknown_wallet_returns_404(self, client):
        resp = client.get(
            "/api/product_metadata?wallet=UNKNOWN&product_id=PCI_AI_001"
        )
        assert resp.status_code == 404

    def test_unknown_product_id_returns_404(self, client):
        resp = client.get(
            "/api/product_metadata?wallet=Base&product_id=DOESNOTEXIST"
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/real_time_liquidity
# ---------------------------------------------------------------------------
class TestRealTimeLiquidity:
    def test_returns_200(self, client):
        assert client.get("/api/real_time_liquidity").status_code == 200

    def test_returns_dict(self, client):
        data = resp_json(client.get("/api/real_time_liquidity"))
        assert isinstance(data, dict)

    def test_all_divisions_present(self, client):
        data = resp_json(client.get("/api/real_time_liquidity"))
        assert "Quantum AI : Market Liquidity Engine" in data

    def test_pool_depth_is_positive_float(self, client):
        data = resp_json(client.get("/api/real_time_liquidity"))
        for division_data in data.values():
            for product_data in division_data.values():
                depth = product_data["pool_depth"]
                assert isinstance(depth, float)
                assert depth > 0


# ---------------------------------------------------------------------------
# 404 handler
# ---------------------------------------------------------------------------
class TestNotFound:
    def test_unknown_route_returns_404(self, client):
        assert client.get("/nonexistent").status_code == 404

    def test_404_body_contains_error_key(self, client):
        data = resp_json(client.get("/nonexistent"))
        assert "error" in data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def resp_json(response) -> dict | list:
    return json.loads(response.data)
