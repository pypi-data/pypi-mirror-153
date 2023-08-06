from unittest import mock
import pytest


@mock.patch('google.cloud.storage.Client', mock.Mock())
@pytest.mark.openedx
def test_plugin_production_settings():
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.production import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_CLIENT=None,
        SITE_CONFIG_CACHE_NAME='default',
        SITE_CONFIG_CACHE_TIMEOUT=3600,
        SITE_CONFIG_BASE_URL="http://service",
        SITE_CONFIG_ENVIRONMENT="staging",
        SITE_CONFIG_API_TOKEN="some-token",
        SITE_CONFIG_READ_ONLY_BUCKET="random-bucket",
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT, 'Client should be initialized'
    assert settings.SITE_CONFIG_CLIENT.read_only_storage, (
        'GCP storage is initialized')
    assert settings.SITE_CONFIF_CLIENT.cache, 'Cache is initialized'


@mock.patch('google.cloud.storage.Client', mock.Mock())
@pytest.mark.openedx
def test_plugin_production_settings_no_gcp(caplog):
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.production import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_CLIENT=None,
        SITE_CONFIG_CACHE_NAME='default',
        SITE_CONFIG_CACHE_TIMEOUT=3600,
        SITE_CONFIG_BASE_URL="http://service",
        SITE_CONFIG_ENVIRONMENT="staging",
        SITE_CONFIG_API_TOKEN="some-token",
        SITE_CONFIG_READ_ONLY_BUCKET=None,
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT, 'Client should be initialized'
    assert not settings.SITE_CONFIG_CLIENT.read_only_storage, (
        'GCP storage should not be initialized because SITE_CONFIG_READ_ONLY_BUCKET is not provided')
    assert settings.SITE_CONFIF_CLIENT.cache, 'Cache is initialized'

    assert 'Not initializing Google storage' in caplog.text


@pytest.mark.openedx
def test_plugin_production_settings_no_client(caplog):
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.production import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_BASE_URL=None,
        SITE_CONFIG_READ_ONLY_BUCKET=None,
    )
    plugin_settings(settings)
    assert settings.SITE_CONFIG_CLIENT, 'Client should not be initialized due to missing SITE_CONFIG_BASE_URL'

    assert 'Not initializing SITE_CONFIG_CLIENT' in caplog.text


@pytest.mark.openedx
def test_plugin_test_settings(client):
    # Local import to avoid test failures for non-openedx tests
    from site_config_client.openedx.settings.test import plugin_settings

    settings = mock.Mock(
        SITE_CONFIG_CLIENT=None,
    )

    plugin_settings(settings)

    assert settings.SITE_CONFIG_CLIENT, 'Client should be initialized'
    assert not settings.SITE_CONFIG_CLIENT.read_only_storage
    assert not settings.SITE_CONFIG_CLIENT.cache
