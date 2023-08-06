"""
Test settings for the Open edX
"""

from site_config_client import Client


def plugin_settings(settings):
    """
    Initialize a client that won't work. Useful for testing, but still needs mocking when used.
    """
    api_token = 'not real token'  # nosec

    settings.SITE_CONFIG_CLIENT = Client(
        base_url='http://localhost:14000/v1/client/',
        api_token=api_token,
        environment='test',
    )
