import json

import requests
from typing import Union
import uuid
from urllib.parse import urljoin

from .exceptions import SiteConfigurationError


STATUS_LIVE = 'live'


def get_cache_key_for_site(site_uuid: Union[str, uuid.UUID]):
    """
    Get the cache key for a site.
    """
    return 'site_config_client.backend.{site_uuid}'.format(
        site_uuid=site_uuid,
    )


class Client:
    def __init__(self, base_url, api_token, environment,
                 read_only_storage=None, cache=None, request_timeout=30):
        """
        Instantiate a new API Client
        """
        self.base_url = base_url
        self.api_token = api_token
        self.environment = environment
        self.read_only_storage = read_only_storage
        self.cache = cache
        self.request_timeout = request_timeout

    def request(self, method, url_path, success_status_code=200, **kwargs):
        """
        Send requests to the Site Configuration service and handle errors.

        Sets timeout and accepts a relative URL.
        """
        headers = {'Authorization': 'Token {}'.format(self.api_token)}
        response = requests.request(
            method=method,
            url=urljoin(self.base_url, url_path),
            timeout=self.request_timeout,
            headers=headers,
            **kwargs
        )

        if response.status_code == success_status_code:
            return response.json()
        else:
            raise SiteConfigurationError((
                'Something went wrong with the site configuration API '
                '`{path}` with status_code="{status_code}" body="{body}"'
            ).format(
                path=url_path,
                status_code=response.status_code,
                body=response.content,
            ))

    def create_site(self, domain_name: str, site_uuid=None):
        """
        Create a new site.
        """
        params = {'domain_name': domain_name}
        if site_uuid:
            params['uuid'] = site_uuid
        url = 'v1/environment/{}/site/'.format(self.environment)
        return self.request('post', url, success_status_code=201, json=params)

    def list_sites(self):
        """
        Returns a list of all Sites
        """
        url = 'v1/environment/{}/site/'.format(self.environment)
        return self.request('get', url)

    def list_active_sites(self):
        """
        Returns a list of all active Sites
        """
        url = 'v1/environment/{}/site/?is_active=True'.format(self.environment)
        return self.request('get', url)

    def get_backend_configs_from_readonly_storage(self, site_uuid: Union[str, uuid.UUID], status: str):
        """
        Reads configuration from read-only storage if available for `live` status only.
        """
        if status != STATUS_LIVE:
            # The read-only storage makes sense only for live (published) configs.
            return None

        file_path = 'v1/backend_configs_live_{site_uuid}.json'.format(site_uuid=site_uuid)

        config_str = None
        if self.read_only_storage:
            config_str = self.read_only_storage.read(file_path)

        if config_str:
            return json.loads(config_str)

        return None

    def get_backend_configs_from_api(self, site_uuid: Union[str, uuid.UUID], status: str):
        """
        Get the backend config from the Site Configuration Service API.
        """
        api_endpoint = 'v1/environment/{}/combined-configuration/backend/{}/{}/'.format(
            self.environment, site_uuid, status
        )
        return self.request('get', url_path=api_endpoint)

    def get_backend_configs_from_cache(self, site_uuid: Union[str, uuid.UUID], status: str):
        """
        Get the backend config from the cache -- if available.
        """
        config = None
        if self.cache and status == STATUS_LIVE:
            # Only cache live status configs. Draft should always be fetched fresh.
            config = self.cache.get(key=get_cache_key_for_site(site_uuid))
        return config

    def set_backend_configs_in_cache(self, site_uuid: Union[str, uuid.UUID], status: str, config):
        """
        Store the config in cache.
        """
        if self.cache and status == STATUS_LIVE:
            # Only cache live status configs. Draft should always be fetched fresh.
            self.cache.set(key=get_cache_key_for_site(site_uuid), value=config)

    def delete_cache_for_site(self, site_uuid: Union[str, uuid.UUID], status):
        """
        Clear cache entry for a specific site.
        """
        if self.cache and status == STATUS_LIVE:
            # Only cache live status configs. Draft should always be fetched fresh.
            self.cache.delete(key=get_cache_key_for_site(site_uuid))

    def get_backend_configs(self, site_uuid: Union[str, uuid.UUID], status: str):
        """
        Returns a combination of Site information and `live` or `draft`
        Configurations (backend secrets included)

        [Client Configuration]
        - Django Cache
            - if cache key exists: return config from cache
            - if cache key does not exist: call endpoint to get config, set
              cache with config, return config
        """
        config = self.get_backend_configs_from_cache(site_uuid, status)

        if config:
            store_in_cache = False
        else:
            store_in_cache = True
            config = self.get_backend_configs_from_readonly_storage(site_uuid, status)

        if not config:
            config = self.get_backend_configs_from_api(site_uuid, status)

        if store_in_cache:
            self.set_backend_configs_in_cache(site_uuid, status, config)

        return config

    def get_config(self, site_uuid: Union[str, uuid.UUID],
                   type: str, name: str, status: str):
        """
        Returns a single configuration object for Site
        """
        api_endpoint = 'v1/environment/{}/configuration/{}/'.format(self.environment, site_uuid)
        return self.request('get', url_path=api_endpoint, json={
            "type": type,
            "name": name,
            "status": status
        })

    def override_configs(self, site_uuid: Union[str, uuid.UUID], configs):
        """
        Override all live configs in a single pass.

        This uses the v0 API which should be deprecated after the initial
        rollout.
        """
        api_endpoint = 'v0/configuration-override/{}/'.format(site_uuid)
        return self.request('put', url_path=api_endpoint, json=configs)
