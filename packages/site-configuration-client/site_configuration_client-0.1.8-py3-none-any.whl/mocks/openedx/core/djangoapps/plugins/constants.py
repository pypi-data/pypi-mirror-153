"""
Mocks for openedx.core.djangoapps.plugins.constants.

Mocks to make the plugin app works during tests
without being concerned to actually test the plugin configs.
"""

from unittest.mock import Mock

# Minimal mocks to reduce test maintenance costs.
SettingsType = Mock()
ProjectType = Mock()
PluginSettings = Mock()
