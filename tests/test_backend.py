"""
Pytest test suite for the Positive Change Institute backend.

Runs against an in-memory Flask test client so no external services are needed.
"""

import json
import pytest

# ---------------------------------------------------------------------------
# Shared test data
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

DIVISIONS_REGISTRY_WITH_POOLS = [
    {
        "name": "XRPL : NFT Liquidity Ecosystem",
        "chain": "XRPL",
        "product_ids": ["PCI_XRPL_001", "PCI_XRPL_002"],
        "pool_addresses": {"PCI_XRPL_001": "rhz5LkGZXz4fEs5T9neWtXC2vJpRVLoXVB"},
    },
]

NFT_CATALOG_TEST = [
    {
        "collection": "Arcana Enterprise Forge\u00ae",
        "tier": "Adaptive",
        "product_id": "FORGE-001",
        "one_time_price_usd": 999,
        "subscription_tiers": {"builder": 9, "studio": 99},
        "auto_evolution": True,
        "ai_powered": "Prometheus",
        "enterprise_utility": ["Dashboard integration"],
        "story_integration": True,
        "rarity": "adaptive",
        "diversification": ["Procedurally generated traits"],
        "motif": "Test motif",
        "evolution_paths": [{"level": 1, "traits": ["Core glyph"]}],
        "qr_code": "QR_TEST",
        "wallet_link": "xrpl://rTest",
        "storefront_link": "https://test.example.com/FORGE-001",
        "copyright_trademark": "\u00a9 2026 PCI",
    }
]


# ---------------------------------------------------------------------------
# App fixtures
# ---------------------------------------------------------------------------
@pytest.fixture()
def app():
    from backend.app import create_app

    flask_app = create_app(
        {
            "WALLET_REGISTRY": WALLET_REGISTRY,
            "DIVISIONS_REGISTRY": DIVISIONS_REGISTRY,
            "NFT_CATALOG": NFT_CATALOG_TEST,
        }
    )
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_with_pools():
    """App fixture with pool_addresses configured for liquidity service tests."""
    from backend.app import create_app

    flask_app = create_app(
        {
            "WALLET_REGISTRY": WALLET_REGISTRY,
            "DIVISIONS_REGISTRY": DIVISIONS_REGISTRY_WITH_POOLS,
            "NFT_CATALOG": NFT_CATALOG_TEST,
        }
    )
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture()
def pool_client(app_with_pools):
    return app_with_pools.test_client()


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

    def test_each_product_record_has_required_fields(self, client):
        data = resp_json(client.get("/api/real_time_liquidity"))
        for division_data in data.values():
            for record in division_data.values():
                assert "pool_depth" in record
                assert "source" in record
                assert "fetched_at" in record

    def test_unconfigured_products_have_no_pool_source(self, client):
        data = resp_json(client.get("/api/real_time_liquidity"))
        # The base test fixture has no pool_addresses, so all products are unconfigured
        for division_data in data.values():
            for record in division_data.values():
                assert record["source"] == "no_pool_configured"
                assert record["pool_depth"] is None


# ---------------------------------------------------------------------------
# GET /api/real_time_liquidity — with pool addresses + mocked HTTP
# ---------------------------------------------------------------------------
class TestRealTimeLiquidityWithPools:
    def test_live_fetch_on_xrpl_success(self, pool_client, mocker):
        mock_resp = mocker.MagicMock()
        mock_resp.json.return_value = {
            "result": {"account_data": {"Balance": "100000000"}}
        }
        mock_resp.raise_for_status = mocker.MagicMock()
        mocker.patch(
            "backend.services.liquidity.requests.post", return_value=mock_resp
        )
        # Clear the module-level cache so fresh fetch is attempted
        from backend.services.liquidity import _cache
        _cache.clear()

        data = resp_json(pool_client.get("/api/real_time_liquidity"))
        xrpl_div = data["XRPL : NFT Liquidity Ecosystem"]
        record = xrpl_div["PCI_XRPL_001"]
        assert record["source"] == "live"
        assert record["pool_depth"] == 100.0
        assert record["fetched_at"] is not None

    def test_unconfigured_product_returns_no_pool(self, pool_client, mocker):
        mocker.patch(
            "backend.services.liquidity.requests.post", return_value=mocker.MagicMock()
        )
        data = resp_json(pool_client.get("/api/real_time_liquidity"))
        # PCI_XRPL_002 has no pool address configured
        record = data["XRPL : NFT Liquidity Ecosystem"]["PCI_XRPL_002"]
        assert record["source"] == "no_pool_configured"
        assert record["pool_depth"] is None

    def test_fallback_to_unavailable_on_fetch_error(self, pool_client, mocker):
        from backend.services.liquidity import _cache
        _cache.clear()
        mocker.patch(
            "backend.services.liquidity.requests.post",
            side_effect=Exception("network timeout"),
        )
        data = resp_json(pool_client.get("/api/real_time_liquidity"))
        record = data["XRPL : NFT Liquidity Ecosystem"]["PCI_XRPL_001"]
        assert record["source"] in ("unavailable", "stale_cache")
        assert record["pool_depth"] is None


# ---------------------------------------------------------------------------
# GET /api/nft/collections
# ---------------------------------------------------------------------------
class TestNFTCollections:
    def test_returns_200(self, client):
        assert client.get("/api/nft/collections").status_code == 200

    def test_returns_list(self, client):
        data = resp_json(client.get("/api/nft/collections"))
        assert isinstance(data, list)
        assert len(data) > 0

    def test_each_entry_has_required_fields(self, client):
        data = resp_json(client.get("/api/nft/collections"))
        for nft in data:
            for field in (
                "collection",
                "tier",
                "product_id",
                "one_time_price_usd",
                "auto_evolution",
                "enterprise_utility",
            ):
                assert field in nft, f"Missing '{field}' in NFT {nft.get('product_id')}"

    def test_detail_returns_200_for_valid_id(self, client):
        assert client.get("/api/nft/collections/FORGE-001").status_code == 200

    def test_detail_returns_correct_entry(self, client):
        data = resp_json(client.get("/api/nft/collections/FORGE-001"))
        assert data["product_id"] == "FORGE-001"
        assert data["tier"] == "Adaptive"

    def test_detail_returns_404_for_unknown_id(self, client):
        assert client.get("/api/nft/collections/UNKNOWN-999").status_code == 404


# ---------------------------------------------------------------------------
# POST /api/prometheus/execute
# ---------------------------------------------------------------------------
class TestPrometheus:
    def test_returns_200_with_valid_task(self, client):
        resp = client.post(
            "/api/prometheus/execute",
            json={"task": "Analyze XRPL liquidity trends"},
        )
        assert resp.status_code == 200

    def test_returns_400_without_task(self, client):
        resp = client.post("/api/prometheus/execute", json={})
        assert resp.status_code == 400

    def test_response_has_required_fields(self, client):
        data = resp_json(
            client.post(
                "/api/prometheus/execute",
                json={"task": "test", "division": "XRPL"},
            )
        )
        for field in ("task", "division", "result", "model", "status", "timestamp"):
            assert field in data, f"Missing field '{field}'"

    def test_demo_mode_when_no_api_key(self, client, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("GROK_API_KEY", raising=False)
        data = resp_json(
            client.post(
                "/api/prometheus/execute",
                json={"task": "test task"},
            )
        )
        assert data["model"] == "demo"
        assert "[DEMO]" in data["result"]

    def test_task_and_division_echoed(self, client):
        data = resp_json(
            client.post(
                "/api/prometheus/execute",
                json={"task": "run analysis", "division": "Quantum AI"},
            )
        )
        assert data["task"] == "run analysis"
        assert data["division"] == "Quantum AI"

    def test_status_is_ok(self, client):
        data = resp_json(
            client.post("/api/prometheus/execute", json={"task": "test"})
        )
        assert data["status"] == "ok"


# ---------------------------------------------------------------------------
# GET /api/analytics/summary
# ---------------------------------------------------------------------------
class TestAnalytics:
    def test_returns_200(self, client):
        assert client.get("/api/analytics/summary").status_code == 200

    def test_has_required_fields(self, client):
        data = resp_json(client.get("/api/analytics/summary"))
        for field in (
            "division_count",
            "wallet_count",
            "total_product_ids",
            "nft_collection_count",
            "gamification_tier_count",
            "api_version",
            "generated_at",
        ):
            assert field in data, f"Missing field '{field}'"

    def test_division_count_matches_registry(self, client):
        data = resp_json(client.get("/api/analytics/summary"))
        assert data["division_count"] == len(DIVISIONS_REGISTRY)

    def test_wallet_count_matches_registry(self, client):
        data = resp_json(client.get("/api/analytics/summary"))
        assert data["wallet_count"] == len(WALLET_REGISTRY)

    def test_nft_count_matches_catalog(self, client):
        data = resp_json(client.get("/api/analytics/summary"))
        assert data["nft_collection_count"] == len(NFT_CATALOG_TEST)


# ---------------------------------------------------------------------------
# GET /api/gamification/tiers
# ---------------------------------------------------------------------------
class TestGamification:
    def test_returns_200(self, client):
        assert client.get("/api/gamification/tiers").status_code == 200

    def test_returns_list(self, client):
        data = resp_json(client.get("/api/gamification/tiers"))
        assert isinstance(data, list)
        assert len(data) == 3  # Adaptive, Mythic, Legendary

    def test_each_tier_has_required_fields(self, client):
        data = resp_json(client.get("/api/gamification/tiers"))
        for tier in data:
            for field in (
                "tier",
                "collection",
                "required_nft_product_id",
                "one_time_entry_usd",
                "subscription_usd_month",
                "api_rate_multiplier",
                "feature_unlocks",
            ):
                assert field in tier, f"Missing '{field}' in tier {tier.get('tier')}"

    def test_detail_valid_tier(self, client):
        resp = client.get("/api/gamification/tiers/Mythic")
        assert resp.status_code == 200
        data = resp_json(resp)
        assert data["tier"] == "Mythic"

    def test_detail_case_insensitive(self, client):
        assert client.get("/api/gamification/tiers/legendary").status_code == 200

    def test_detail_invalid_tier_returns_404(self, client):
        resp = client.get("/api/gamification/tiers/Nonexistent")
        assert resp.status_code == 404
        data = resp_json(resp)
        assert "valid_tiers" in data


# ---------------------------------------------------------------------------
# GET /api/tokenomics/model
# ---------------------------------------------------------------------------
class TestTokenomics:
    def test_default_params_return_200(self, client):
        assert client.get("/api/tokenomics/model").status_code == 200

    def test_response_has_required_fields(self, client):
        data = resp_json(client.get("/api/tokenomics/model"))
        for field in (
            "supply",
            "initial_price_usd",
            "public_distribution",
            "circulating_supply",
            "market_cap_usd",
            "fully_diluted_valuation_usd",
            "liquidity_depth_estimate_usd",
            "vesting_schedule",
            "model",
        ):
            assert field in data, f"Missing field '{field}'"

    def test_custom_params_are_reflected(self, client):
        data = resp_json(
            client.get(
                "/api/tokenomics/model?supply=2000000&initial_price=0.05&distribution=0.4"
            )
        )
        assert data["supply"] == 2_000_000
        assert data["initial_price_usd"] == 0.05
        assert data["public_distribution"] == 0.4
        assert data["circulating_supply"] == 800_000

    def test_market_cap_calculation(self, client):
        data = resp_json(
            client.get(
                "/api/tokenomics/model?supply=1000000&initial_price=1.0&distribution=0.5"
            )
        )
        assert data["market_cap_usd"] == 500_000.0

    def test_invalid_supply_returns_400(self, client):
        assert (
            client.get("/api/tokenomics/model?supply=-1").status_code == 400
        )

    def test_zero_supply_returns_400(self, client):
        assert (
            client.get("/api/tokenomics/model?supply=0").status_code == 400
        )

    def test_invalid_distribution_returns_400(self, client):
        assert (
            client.get("/api/tokenomics/model?distribution=1.5").status_code == 400
        )

    def test_vesting_schedule_is_list(self, client):
        data = resp_json(client.get("/api/tokenomics/model"))
        assert isinstance(data["vesting_schedule"], list)
        assert data["vesting_schedule"][-1]["circulating_pct"] == 1.0


# ---------------------------------------------------------------------------
# GET /api/compliance/check
# ---------------------------------------------------------------------------
class TestCompliance:
    def test_valid_xrpl_address_returns_clear(self, client):
        resp = client.get(
            "/api/compliance/check"
            "?address=rhz5LkGZXz4fEs5T9neWtXC2vJpRVLoXVB&chain=XRPL"
        )
        assert resp.status_code == 200
        data = resp_json(resp)
        assert data["format_valid"] is True
        assert data["status"] == "clear"
        assert data["risk_flags"] == []

    def test_valid_eth_address_returns_clear(self, client):
        resp = client.get(
            "/api/compliance/check"
            "?address=0xAbCdEf1234567890abcdef1234567890AbCdEf12&chain=ETH"
        )
        assert resp.status_code == 200
        data = resp_json(resp)
        assert data["format_valid"] is True
        assert data["status"] == "clear"

    def test_invalid_format_returns_invalid_format(self, client):
        resp = client.get(
            "/api/compliance/check?address=not_an_address&chain=XRPL"
        )
        assert resp.status_code == 200
        data = resp_json(resp)
        assert data["format_valid"] is False
        assert data["status"] == "invalid_format"

    def test_burn_address_is_flagged(self, client):
        resp = client.get(
            "/api/compliance/check"
            "?address=0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef&chain=ETH"
        )
        assert resp.status_code == 200
        data = resp_json(resp)
        assert "burn_address" in data["risk_flags"]
        assert data["status"] == "flagged"

    def test_missing_params_returns_400(self, client):
        assert client.get("/api/compliance/check").status_code == 400
        assert client.get("/api/compliance/check?address=r123").status_code == 400

    def test_response_has_required_fields(self, client):
        data = resp_json(
            client.get(
                "/api/compliance/check"
                "?address=rhz5LkGZXz4fEs5T9neWtXC2vJpRVLoXVB&chain=XRPL"
            )
        )
        for field in ("address", "chain", "format_valid", "risk_flags", "status", "checked_at"):
            assert field in data, f"Missing field '{field}'"


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
