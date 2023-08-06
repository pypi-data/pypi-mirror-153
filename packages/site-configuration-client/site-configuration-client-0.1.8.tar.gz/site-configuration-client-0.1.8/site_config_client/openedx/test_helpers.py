"""
Test helpers for other packages to override testers.
"""

from unittest.mock import patch, Mock


def override_site_config(config_type, **config_overrides):
    """
    Override site config settings for a specific type of configuration.
    """
    def overrider_for_get_value_of_type(name, default=None, site_configuration=None):
        return config_overrides.get(name, default)

    return patch(
        'site_config_client.openedx.api.get_{type}_value'.format(type=config_type),
        Mock(side_effect=overrider_for_get_value_of_type),
    )
