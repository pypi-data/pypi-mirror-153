"""
Tests for site_config_client.openedx.test_helpers
"""
import pytest

try:
    from site_config_client.openedx.test_helpers import override_site_config
    from site_config_client.openedx import api as openedx_api
except ImportError:
    # Silent import failures for non-Open edX environments.
    pass


@pytest.mark.openedx
def test_secret_override():
    """
    Use `override_site_config` for a `secret` site configuration.
    """
    with override_site_config('secret', EMAIL_PASSWORD='test'):
        assert openedx_api.get_secret_value('EMAIL_PASSWORD') == 'test'


@pytest.mark.openedx
def test_without_overrides_fails():
    """
    Test that api fails without overrides due to missing packages in test environment.
    """

    with pytest.raises(NameError, match='name .configuration_helpers. is not defined'):
        openedx_api.get_secret_value('EMAIL_PASSWORD')
