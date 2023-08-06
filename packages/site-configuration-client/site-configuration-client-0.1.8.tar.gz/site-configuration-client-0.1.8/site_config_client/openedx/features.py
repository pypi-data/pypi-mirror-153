"""
Feature helpers for Open edX.
"""

from django.conf import settings

from site_config_client.models import SiteConfigClientEnabled


def is_feature_enabled():
    """
    Checks if the feature is globally enabled.
    """
    enabled_globally = settings.FEATURES.get('SITE_CONFIG_CLIENT_ENABLED', False)
    return enabled_globally


def enable_feature_for_site(site_uuid, note=''):
    """
    Enable the site configuration client for a site by site_uuid.

    Returns: whether a new flag is created or not.
    """
    _, created = SiteConfigClientEnabled.objects.get_or_create(
        site_uuid=site_uuid,
        defaults={
            'note': note,
        }
    )
    return created


def is_feature_enabled_for_site(site_uuid):
    """
    Checks if feature is globally enabled OR for the specific site.

    This helps to facilitates gradual migration.
    """
    if is_feature_enabled():
        return True

    return SiteConfigClientEnabled.objects.filter(site_uuid=site_uuid).exists()
