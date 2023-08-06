"""
Tests for the openedx.api module.
"""
from unittest.mock import patch, Mock

import pytest

try:
    from site_config_client.openedx import api as openedx_api
except ImportError:
    # Silent import failures for non-Open edX environments.
    pass


def with_current_configs(current_config):
    """
    @patch `get_current_site_configuration()`
    """
    configuration_helpers = Mock()
    configuration_helpers.get_current_site_configuration.return_value = current_config
    return patch(
        'site_config_client.openedx.api.configuration_helpers',
        configuration_helpers,
        create=True,
    )


@pytest.mark.openedx
def test_get_admin_value():
    """
    Test `get_admin_value()` helper for `admin` type of configurations.
    """
    current_config = Mock()
    current_config.get_admin_setting.return_value = 'password'
    with with_current_configs(current_config):
        admin_value = openedx_api.get_admin_value('IDP_CLIENT', 'default-client')
    assert admin_value == 'password'
    current_config.get_admin_setting.assert_called_with('IDP_CLIENT', 'default-client')


@pytest.mark.openedx
def test_get_secret_value():
    """
    Test `get_secret_value()` helper for `secret` type of configurations.
    """
    current_config = Mock()
    current_config.get_secret_value.return_value = 'password'
    with with_current_configs(current_config):
        secret_value = openedx_api.get_secret_value('EMAIL_PASSWORD', 'default-pass')
    assert secret_value == 'password'
    current_config.get_secret_value.assert_called_with('EMAIL_PASSWORD', 'default-pass')


@pytest.mark.openedx
def test_get_setting_value():
    """
    Test `get_setting_value()` helper for `setting` type of configurations.
    """
    current_config = Mock()
    current_config.get_value.return_value = 'pre-defined-site.com'
    with with_current_configs(current_config):
        setting = openedx_api.get_setting_value('SITE_NAME', 'defaultsite.com')
    assert setting == 'pre-defined-site.com'
    current_config.get_value.assert_called_with('SITE_NAME', 'defaultsite.com')


@pytest.mark.openedx
def test_get_page_value():
    """
    Test `get_page_value()` helper for `page` type of configurations.
    """
    current_config = Mock()
    current_config.get_page_content.return_value = '{"title": "About page"}'
    with with_current_configs(current_config):
        page_value = openedx_api.get_page_value('about', {})
    assert page_value == '{"title": "About page"}'
    current_config.get_page_content.assert_called_with('about', {})


@pytest.mark.openedx
@with_current_configs(current_config=None)  # Simulate an environment with no current configuration.
def test_use_default_on_missing_site_configuration():
    """
    Ensure all openedx_api helpers return `default` if `site_configuration` is missing.

    This is useful to return `None` for tests and when running on Open edX's main site.
    """
    assert openedx_api.get_secret_value('TEST_SECRET', 'default_secret') == 'default_secret'
    assert openedx_api.get_admin_value('TEST_CONFIG', 'dummy-default') == 'dummy-default'
    assert openedx_api.get_page_value('TEST_PAGE', 'dummy_page_content') == 'dummy_page_content'
    assert openedx_api.get_setting_value('CUSTOMER_ID', 'dummy-customer') == 'dummy-customer'
