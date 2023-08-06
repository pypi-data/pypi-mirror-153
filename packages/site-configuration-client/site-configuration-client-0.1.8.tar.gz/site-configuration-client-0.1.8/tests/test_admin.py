"""
Tests for adapter
"""
import pytest


@pytest.mark.django
def test_feature_flag_admin():
    """
    Tests for SiteConfigClientEnabledAdmin.
    """
    from site_config_client.admin import SiteConfigClientEnabledAdmin

    assert SiteConfigClientEnabledAdmin.list_display == ['site_uuid', 'note']
    assert SiteConfigClientEnabledAdmin.search_fields == ['site_uuid', 'note']
