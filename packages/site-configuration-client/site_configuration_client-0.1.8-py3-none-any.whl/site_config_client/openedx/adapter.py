"""
"""
from django.conf import settings


AMC_V1_STRUCTURE_VERSION = 'amc-v1'


class SiteConfigAdapter:
    """
    Adapter for Open edX translates the values in a format that Open edX can use.
    """

    backend_configs = None

    TYPE_SETTING = 'setting'
    TYPE_SECRET = 'secret'  # nosec
    TYPE_ADMIN = 'admin'
    TYPE_PAGE = 'page'
    TYPE_CSS = 'css'

    def __init__(self, site_uuid, status='live'):
        self.site_uuid = site_uuid
        self.status = status

    def get_backend_configs(self):
        if not self.backend_configs:
            client = settings.SITE_CONFIG_CLIENT
            self.backend_configs = client.get_backend_configs(self.site_uuid, self.status)
        return self.backend_configs

    def delete_backend_configs_cache(self):
        """
        Enforce getting a fresh entry for the current context/request and following ones.
        """
        self.backend_configs = None
        client = settings.SITE_CONFIG_CLIENT
        client.delete_cache_for_site(self.site_uuid, self.status)

    def get_value_of_type(self, config_type, name, default):
        all_configs = self.get_backend_configs()['configuration']
        type_configs = all_configs[config_type]
        return type_configs.get(name, default)

    def get_amc_v1_theme_css_variables(self):
        """
        Returns an Open edX AMC v1 theme compatible sass variables.

        Note: This function assumes that all variables are compatible with v1 theme.
        """
        config = self.get_backend_configs()['configuration']

        # Imitates the values in edX's SiteConfiguration sass_variables
        openedx_theme_compatible_css_vars = [
            # Note: The usual AMC produced format is key --> [value, default]
            #       The second value is mostly unused by Open edX can be
            #       set as [value, default].
            [key, val]
            for key, val in config[self.TYPE_CSS].items()
        ]
        return openedx_theme_compatible_css_vars
