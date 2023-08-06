"""
Models for the Site Configuration client.
"""

from django.contrib import admin

from .models import SiteConfigClientEnabled


@admin.register(SiteConfigClientEnabled)
class SiteConfigClientEnabledAdmin(admin.ModelAdmin):
    """
    Admin interface for SiteConfigClientEnabled.
    """

    list_display = ['site_uuid', 'note']
    search_fields = ['site_uuid', 'note']
