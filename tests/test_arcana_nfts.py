from arcana_enterprise_nfts.arcana_nfts import arcana_nfts


def test_arcana_nft_catalog_is_importable_and_non_empty():
    assert isinstance(arcana_nfts, list)
    assert arcana_nfts


def test_arcana_nft_catalog_entries_have_boolean_flags():
    for entry in arcana_nfts:
        assert isinstance(entry["auto_evolution"], bool)
        assert isinstance(entry["story_integration"], bool)
