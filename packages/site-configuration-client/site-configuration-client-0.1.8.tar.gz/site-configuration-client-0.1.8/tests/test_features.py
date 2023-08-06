"""
Tests for adapter
"""

from uuid import uuid4
import pytest


@pytest.mark.openedx
def test_global_feature_flag(settings):
    from site_config_client.openedx.features import is_feature_enabled
    assert not is_feature_enabled(), 'Should be disabled by default'

    settings.FEATURES = {'SITE_CONFIG_CLIENT_ENABLED': True}
    assert is_feature_enabled(), 'Should be enabled because of feature flag'


@pytest.mark.openedx
@pytest.mark.django_db
def test_site_feature_flags_with_global_flag(settings):
    from site_config_client.openedx.features import is_feature_enabled_for_site
    site_uuid = uuid4()

    assert not is_feature_enabled_for_site(site_uuid), 'Should be disabled by default'

    settings.FEATURES = {'SITE_CONFIG_CLIENT_ENABLED': True}
    assert is_feature_enabled_for_site(site_uuid), 'Should be enabled because of global feature flag'


@pytest.mark.openedx
@pytest.mark.django_db
def test_site_feature_flags_without_global_flag():
    from site_config_client.models import SiteConfigClientEnabled
    from site_config_client.openedx import features
    site_uuid = uuid4()

    assert not features.is_feature_enabled_for_site(site_uuid), 'Should be disabled by default'
    assert not SiteConfigClientEnabled.objects.filter(site_uuid=site_uuid).exists()

    features.enable_feature_for_site(site_uuid=site_uuid)

    assert SiteConfigClientEnabled.objects.filter(site_uuid=site_uuid).exists(), 'enable_feature_for_site adds it'
    assert features.is_feature_enabled_for_site(site_uuid), 'Should be enabled because of site-specific feature flag'


@pytest.mark.openedx
@pytest.mark.django_db
def test_enable_feature_for_site_with_note():
    from site_config_client.models import SiteConfigClientEnabled
    from site_config_client.openedx import features

    site_uuid = uuid4()
    assert features.enable_feature_for_site(site_uuid=site_uuid, note='my note'), 'should create new entry'
    assert not features.enable_feature_for_site(site_uuid=site_uuid), 'should keep the old entry'
    assert features.is_feature_enabled_for_site(site_uuid), 'calling the helper twice do not hurt'
    flag = SiteConfigClientEnabled.objects.get(site_uuid=site_uuid)
    assert flag.note == 'my note', 'enable_feature_for_site can add a note'
