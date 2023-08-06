"""
Tests for Client
"""
import json

from unittest.mock import Mock
import pytest

from site_config_client import Client
from site_config_client.django_cache import DjangoCache
from site_config_client.exceptions import SiteConfigurationError


SITES = {
    "count": 2,
    "results": [
            {
                "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
                "domain_name": "croissant.edu",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            },
            {
                "uuid": "040e0ec3-2578-4fcf-b5db-030dadf68f30",
                "domain_name": "test-site.com",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            }
        ]
}


CONFIGS = {
    "site": {
                "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
                "domain_name": "croissant.edu",
                "tier": "trial",
                "always_active": "False",
                "subscription_ends": "2021-10-31T16:44:45+0000",
                "is_active": "True"
            },
    "status": "draft",
    "configuration":
        {
            "css": [
                    {"name": "accent-font",
                     "value": "monospace"}
                    ],
            "page": [],
            "setting": [
                        {"name": "PLATFORM_NAME",
                         "value": "Momofuku Academy"}
                        ],
            "integration": [],
            "secret": [],
            "admin": [
                      {"name": "features",
                       "value": ["bi_connector", "google_tag_manageer"]}
                    ]
        }
}


SINGLE_CONFIG = {
        "site_uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
        "name": "PLATFORM_NAME",
        "value": "Academy of Modern Arts",
        "author_email": "test@example.com",
        "structure_version": "amc-v1",
        "modified": "2021-09-30T16:00:42+0000"
    }


OVERRIDE_CONFIGS = {
        'author_email': 'test@example.com',
        'css': [{
            'name': '$brand-primary-color',
            'value': ['rgba(0,1,1,1)', 'rgba(0,1,1,1)']
        }]
    }


PARAMS = {
    "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce"
}


def test_client():
    base = "http://127.0.0.1:8000"
    token = "abcaseasyas123"
    bucket = "http://storage.googleapis.com/appsembler/site_config"
    environment = 'staging'
    c = Client(base_url=base,
               api_token=token,
               environment=environment,
               read_only_storage=bucket,
               request_timeout=100,)

    assert c.base_url == base
    assert c.api_token == token
    assert c.environment == environment
    assert c.read_only_storage == bucket
    assert c.request_timeout == 100, 'should not be a tuple'


@pytest.fixture
def site_config_client():
    client = Client(
                base_url="http://service",
                api_token="some-token",
                environment="staging",
    )
    return client


def test_client_has_token(site_config_client):
    assert site_config_client.api_token, 'Client should have an API token'


def test_create_site(site_config_client, requests_mock):
    headers = {'Authorization': '{}'.format(site_config_client.api_token)}
    uuid = 'f12293e5-46b1-46f0'
    site_path = 'http://service/v1/environment/staging/site/'
    requests_mock.post(site_path, json={'site_uuid': uuid},
                       headers=headers, status_code=201)
    new_site = site_config_client.create_site(domain_name='example.com',
                                              site_uuid=uuid)
    assert new_site == {'site_uuid': uuid}
    history = requests_mock.request_history[0]
    assert history.headers.get('Authorization') == 'Token some-token', (
        'API Token passed in Authorization header')


def test_create_site_with_error(site_config_client, requests_mock):
    headers = {'Authorization': '{}'.format(site_config_client.api_token)}

    site_path = 'http://service/v1/environment/staging/site/'
    requests_mock.post(site_path, json={'site_uuid': 'f12293e5-46b1-46f0'},
                       headers=headers, status_code=400)

    with pytest.raises(SiteConfigurationError):
        site_config_client.create_site(domain_name='example.com')

    history = requests_mock.request_history[0]
    assert history.headers.get('Authorization') == 'Token some-token', (
        'API Token passed in Authorization header')


def test_list_sites(site_config_client, requests_mock):
    headers = {'Authorization': '{}'.
               format(site_config_client.api_token)}

    site_path = "http://service/v1/environment/staging/site/"
    requests_mock.get(site_path, json=SITES, headers=headers, status_code=200)
    response_sites = site_config_client.list_sites()
    assert response_sites == SITES
    history = requests_mock.request_history[0]
    assert history.headers.get("Authorization") == "Token some-token", (
        "API Token passed in Authorization header")


def test_list_sites_with_error(site_config_client, requests_mock):
    site_path = "http://service/v1/environment/staging/site/"
    requests_mock.get(site_path, json=SITES, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.list_sites()


def test_list_active_sites(site_config_client, requests_mock):
    headers = {'Authorization': '{}'.
               format(site_config_client.api_token)}

    active_sites_path = "http://service/v1/environment/staging/site/?is_active=True"
    requests_mock.get(active_sites_path, json=SITES, headers=headers,
                      status_code=200)
    response_active_sites = site_config_client.list_active_sites()
    assert response_active_sites == SITES
    history = requests_mock.request_history[0]
    assert history.headers.get("Authorization") == "Token some-token", (
        "API Token passed in Authorization header")


def test_list_active_sites_error(site_config_client, requests_mock):
    active_sites_path = "http://service/v1/environment/staging/site/?is_active=True"
    requests_mock.get(active_sites_path, json=SITES, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.list_active_sites()


def test_get_backend_configs(requests_mock, site_config_client):
    headers = {'Authorization': '{}'.
               format(site_config_client.api_token)}

    backend_draft_configs_path = (
        'http://service/v1/environment/staging/combined-configuration/backend/{}/draft/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_draft_configs_path,
                      json=CONFIGS, headers=headers, status_code=200)
    response_configs = site_config_client.get_backend_configs(
        site_uuid=PARAMS['uuid'], status='draft')
    assert response_configs == CONFIGS, (
        'Neither cache nor google cloud storage configured')
    history = requests_mock.request_history[0]
    assert history.headers.get("Authorization") == "Token some-token", (
        "API Token passed in Authorization header")


def test_get_backend_configs_error(requests_mock, site_config_client):
    backend_draft_configs_path = (
        'http://service/v1/environment/staging/combined-configuration/backend/{}/draft/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_draft_configs_path,
                      json=CONFIGS, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.get_backend_configs(
            site_uuid=PARAMS['uuid'], status='draft')


@pytest.mark.django
def test_get_backend_configs_cache(requests_mock, site_config_client):
    site_config_client.cache = DjangoCache(cache_name='default')
    backend_live_configs_path = (
        'http://service/v1/environment/staging/combined-configuration/backend/{}/live/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_live_configs_path,
                      json=CONFIGS, status_code=200)

    cache_key = 'site_config_client.backend.{}'.format(PARAMS['uuid'])
    config = site_config_client.cache.get(key=cache_key)
    assert config is None, 'Cache does not exist'

    # First read without cache
    fresh_configs = site_config_client.get_backend_configs(
        site_uuid=PARAMS['uuid'], status='live')
    cache_config_value = site_config_client.cache.get(key=cache_key)
    assert cache_config_value == fresh_configs, 'Cache key has been set'

    # Second read with cache
    cached_configs = site_config_client.get_backend_configs(
        site_uuid=PARAMS['uuid'], status='live')
    assert cached_configs == fresh_configs, 'Reading from cache returns the same result'

    # Remove the cache
    site_config_client.delete_cache_for_site(site_uuid=PARAMS['uuid'], status='live')
    assert not site_config_client.get_backend_configs_from_cache(
        site_uuid=PARAMS['uuid'],
        status='live',
    ), 'Should be deleted'


@pytest.mark.django
def test_get_backend_configs_readonly_storage(requests_mock, site_config_client):
    read_only_storage_configs = {
        "site": {
            "uuid": "77d4ee4e-6888-4965-b246-b8629ac65bce",
            "domain_name": "croissant.edu",
            "tier": "trial",
            "always_active": "False",
            "subscription_ends": "2021-10-31T16:44:45+0000",
            "is_active": "True"
        },
        "status": "live",
        "configuration": {}
    }
    storage = Mock()
    storage.read.return_value = json.dumps(read_only_storage_configs)
    site_config_client.read_only_storage = storage
    backend_draft_configs_path = (
        'http://service/v1/environment/staging/combined-configuration/backend/{}/draft/'
        .format(PARAMS['uuid']))
    requests_mock.get(backend_draft_configs_path,
                      json=CONFIGS, status_code=200)

    draft_configs = site_config_client.get_backend_configs(site_uuid=PARAMS['uuid'], status='draft')
    assert draft_configs == CONFIGS, 'Should read draft configs from API directly without using the readonly storage'

    live_configs = site_config_client.get_backend_configs(site_uuid=PARAMS['uuid'], status='live')
    storage.read.assert_called_once_with('v1/backend_configs_live_{}.json'.format(PARAMS['uuid']))
    assert live_configs == read_only_storage_configs


def test_get_config(requests_mock, site_config_client):
    headers = {'Authorization': '{}'.
               format(site_config_client.api_token)}

    config_path = "http://service/v1/environment/staging/configuration/{}/".format(PARAMS['uuid'])
    requests_mock.get(config_path, json=SINGLE_CONFIG, headers=headers,
                      status_code=200)
    response_configs = site_config_client.get_config(
        site_uuid=PARAMS['uuid'],
        type="setting",
        name="PLATFORM_NAME",
        status="live")
    assert response_configs == SINGLE_CONFIG
    history = requests_mock.request_history[0]
    assert history.headers.get("Authorization") == "Token some-token", (
        "API Token passed in Authorization header")


def test_get_config_error(requests_mock, site_config_client):
    config_path = "http://service/v1/environment/staging/configuration/{}/".format(PARAMS['uuid'])

    requests_mock.get(config_path,
                      json=SINGLE_CONFIG, status_code=404)

    with pytest.raises(SiteConfigurationError):
        site_config_client.get_config(
            site_uuid=PARAMS['uuid'],
            type="setting",
            name="PLATFORM_NAME",
            status="live")


def test_override_configs(requests_mock, site_config_client):
    headers = {'Authorization': '{}'.
               format(site_config_client.api_token)}

    override_path = (
        "http://service/v0/configuration-override/{}/"
        .format(PARAMS['uuid']))
    success_response = {
        "developer_message": "Configurations has been overriden successfully."
        }
    requests_mock.put(override_path, json=success_response,
                      headers=headers, status_code=200)
    override_response = site_config_client.override_configs(
        site_uuid=PARAMS['uuid'], configs=OVERRIDE_CONFIGS)
    assert override_response == success_response
    history = requests_mock.request_history[0]
    assert history.headers.get("Authorization") == "Token some-token", (
        "API Token passed in Authorization header")


def test_override_configs_error(requests_mock, site_config_client):
    override_path = (
        "http://service/v0/configuration-override/{}/"
        .format(PARAMS['uuid']))

    requests_mock.put(override_path, status_code=500)

    with pytest.raises(SiteConfigurationError):
        site_config_client.override_configs(
            site_uuid=PARAMS['uuid'], configs=OVERRIDE_CONFIGS)
