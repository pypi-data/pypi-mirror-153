"""
Test SiteConfigApp
"""
import pytest

try:
    import openedx  # noqa
    OPENEDX_ENVIRONMENT = True
except ImportError:
    OPENEDX_ENVIRONMENT = False


@pytest.mark.openedx
def test_plugin_config_openedx():
    """
    Check for syntax or other severe errors in SiteConfigApp.plugin_app
    """
    # Local import to avoid test failures for non-openedx tests
    from site_config_client import apps

    config = apps.SiteConfigApp('siteconfig', apps)
    assert type(config.plugin_app) == dict, 'Should have Open edX configs.'


@pytest.mark.django
@pytest.mark.skipif(OPENEDX_ENVIRONMENT, reason='Should not run if `openedx` is available')
def test_plugin_config_django():
    """
    Check for syntax or other severe errors in SiteConfigApp.plugin_app
    """
    # Local import to avoid test failures for non-django tests
    from site_config_client import apps

    config = apps.SiteConfigApp('siteconfig', apps)
    assert not getattr(config, 'plugin_app', None), 'Plugin app should only be available in Open edX environment.'
