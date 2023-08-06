"""
Models for the Site Configuration client.
"""

from django.db import models


class SiteConfigClientEnabled(models.Model):
    """
    A model to enable the site configuration client for a specific site.

    This is mostly used by Open edX, so it's mostly useless for non Open edX projects.
    """

    class Meta:
        app_label = 'site_config_client'

    site_uuid = models.UUIDField(verbose_name='UUID of the site the client enabled for.', unique=True)
    note = models.CharField(verbose_name='Note for the the admin.', max_length=255)
