"""
Production settings for the Open edX
"""
import logging

from site_config_client import Client
from site_config_client.django_cache import DjangoCache


log = logging.getLogger(__name__)


def plugin_settings(settings):
    """
    Production and devstack settings for Site Configuration API Client.
    """

    bucket_name = getattr(settings, 'SITE_CONFIG_READ_ONLY_BUCKET', None)
    read_only_storage = None

    if bucket_name:
        # Google Cloud Storage is optional and used for service reliability
        from site_config_client.google_cloud_storage import GoogleCloudStorage
        read_only_storage = GoogleCloudStorage(
            bucket_name=settings.SITE_CONFIG_READ_ONLY_BUCKET,
        )
    else:
        log.warning('Not initializing Google storage bucket due to missing settings parameter.')

    cache = DjangoCache(
        cache_name=getattr(settings, 'SITE_CONFIG_CACHE_NAME', 'default'),
        cache_timeout=getattr(settings, 'SITE_CONFIG_CACHE_TIMEOUT', None),
    )

    base_url = getattr(settings, 'SITE_CONFIG_BASE_URL', None)
    if base_url:
        settings.SITE_CONFIG_CLIENT = Client(
            base_url=settings.SITE_CONFIG_BASE_URL,
            api_token=settings.SITE_CONFIG_API_TOKEN,
            environment=settings.SITE_CONFIG_ENVIRONMENT,
            read_only_storage=read_only_storage,
            cache=cache,
        )
    else:
        log.warning('Not initializing SITE_CONFIG_CLIENT due to missing parameter.')
