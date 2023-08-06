"""
Tests for adapter
"""
import pytest
from unittest.mock import Mock
from collections import OrderedDict


CONFIGS = {
    "site": {
        "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
    },
    "status": "live",
    "configuration": {
        "css": OrderedDict(
            # Just like a normal dict, but makes tests less flaky
            (
                ("selected_font", ["lato", "lato"]),
                ("text_color", ["#0a0a0a", "#0a0a0a"]),
                ("header_logo_height", ["110", "110"]),
                ("header_buttons_color", ["#164be0", "#164be0"]),
                ("header_font_size", ["17", "17"]),
            )
        ),
        "page": {
            "course-card": "course-tile-01",
            "privacy": {
                "content": [
                    {
                     "element-type": "layout-50:50",
                     "element-path": "page-builder/layouts/_two-col-50-50.html"
                    }
                ]
            }
        },
        "setting": {
            "PLATFORM_NAME": "My New Platform Name!",
            "footer_copyright_text": "© Appsembler 2021. All rights reserved.",
            "display_footer_powered_by": "false",
            "display_footer_legal": "false",
            "google_verification_code": "GoogleVerify!",
            "site_title": "My site title"
        },
        "integration": {},
        "secret": {
            "SEGMENT_KEY": "so secret",
        },
        "admin": {},
        }
}


@pytest.mark.openedx
def test_adapater(settings):
    '''
    I want to mock the return value for `get_backend_config` as CONFIGS
    and test the return values of:
     `get_value`,  `get_amc_v1_theme_css_variables`, `get_amc_v1_page`
    '''
    from site_config_client.openedx.adapter import SiteConfigAdapter

    mock = Mock()
    mock.get_backend_configs.return_value = CONFIGS
    settings.SITE_CONFIG_CLIENT = mock
    adapter = SiteConfigAdapter("77d4ee4e-6888-4965", "live")

    assert adapter.get_backend_configs() == CONFIGS

    setting_platform_name = adapter.get_value_of_type('setting', 'PLATFORM_NAME', None)
    assert setting_platform_name == CONFIGS['configuration']['setting']['PLATFORM_NAME']
    assert adapter.get_value_of_type('secret', 'SEGMENT_KEY', None) == 'so secret'

    css_vars = adapter.get_amc_v1_theme_css_variables()
    # This change is temporary til we migrate off AMC and its edx-customers-theme
    assert css_vars == [
        ["selected_font", ["lato", "lato"]],
        ["text_color", ["#0a0a0a", "#0a0a0a"]],
        ["header_logo_height", ["110", "110"]],
        ["header_buttons_color", ["#164be0", "#164be0"]],
        ["header_font_size", ["17", "17"]],
    ], 'get_amc_v1_theme_css_variables should return AMC-like variables'

    privacy_page_vars = adapter.get_value_of_type('page', 'privacy', None)
    assert privacy_page_vars == CONFIGS['configuration']['page']['privacy']

    assert adapter.get_value_of_type('page', 'non_existent', None) is None, 'Should default to None'
    assert adapter.get_value_of_type('page', 'non_existent', {'title': 'default'}) == {
        'title': 'default',
    }, 'Should has a default'

    assert adapter.backend_configs, 'Sanity check: in-memory cache should be available'
    adapter.delete_backend_configs_cache()
    assert not adapter.backend_configs, 'Should remove in-memory cache'
