"""Tests for NFT minting safeguards."""

import pytest

from arcana_enterprise_nfts.mint import (
    MAINNET_CONFIRMATION,
    SafeguardError,
    check_safeguards,
    select_targets,
)


def test_testnet_within_cap_allowed():
    check_safeguards(False, None, None, 3, 3)


def test_cap_exceeded_blocked():
    with pytest.raises(SafeguardError, match="exceeds cap"):
        check_safeguards(False, None, None, 4, 3)


def test_invalid_cap_blocked():
    with pytest.raises(SafeguardError):
        check_safeguards(False, None, None, 1, 0)


def test_mainnet_needs_phrase():
    with pytest.raises(SafeguardError, match="confirm-mainnet"):
        check_safeguards(True, None, "yes", 1, 3)


def test_mainnet_needs_env_opt_in():
    with pytest.raises(SafeguardError, match="PCI_ALLOW_MAINNET"):
        check_safeguards(True, MAINNET_CONFIRMATION, None, 1, 3)


def test_mainnet_with_both_allowed():
    check_safeguards(True, MAINNET_CONFIRMATION, "YES", 1, 3)


def test_select_targets():
    assert [n["product_id"] for n in select_targets("FORGE-001")] == ["FORGE-001"]
    assert select_targets("NOPE") == []
