# -*- coding: utf-8 -*-
#
#      Copyright (C) 2020 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Thread
from time import sleep

import requests
from requests import RequestException

from axualclient.exception import NoClusterAvailableException
from axualclient.util import dict_to_str
from axualclient.version import __version__

logger = logging.getLogger(__name__)


BACKOFF_PERIOD = 10  # seconds
V2_ENDPOINT_SUFFIX = 'v2'

# Discovery result keys
BOOTSTRAP_SERVERS_KEY = 'bootstrap.servers'
TIMESTAMP_KEY = 'timestamp'
TTL_KEY = 'ttl'
SCHEMA_REGISTRY_URL_KEY = 'schema.registry.url'
DISTRIBUTOR_TIMEOUT_KEY = 'distributor.timeout'
DISTRIBUTOR_DISTANCE_KEY = 'distributor.distance'


class DiscoveryClient(ABC):
    """ DiscoveryAPI observer interface, contains callback for change of properties. """

    @abstractmethod
    def on_discovery_properties_changed(self, discovery_result: dict):
        """ A new discovery result has been received. """
        pass


def _v2_suffix(endpoint: str) -> str:
    """ Appends `/v2` to the endpoint suffix. """
    version_two = V2_ENDPOINT_SUFFIX if endpoint.endswith('/') else '/' + V2_ENDPOINT_SUFFIX
    return endpoint + version_two


class DiscoveryFetcher:
    """ Makes calls against DiscoveryAPI to read the cluster assignment. """

    def __init__(self,
                 config: dict,
                 discovery_client: DiscoveryClient):
        self.endpoint = _v2_suffix(config['endpoint'])
        self.application_id = config['application_id']
        self.application_version = config.get('version', 'unknown')
        self.tenant = config['tenant']
        self.environment = config['environment']
        self.root_ca_location = config['ssl.ca.location']
        self.ssl_key_location = config['ssl.key.location']
        self.ssl_certificate_location = config['ssl.certificate.location']
        self.discovery_clients = []

        self.discovery_result = {}

        self.initialized = False
        # Stop discovery only in case of exceptions
        self.stop_discovery = False
        self._discovery_thread = None
        # Serves as the termination condition if raised prior to a valid discovery response.
        self._initialization_exception = None

        self.__start_continuous_discovery_thread()
        self.register_discovery_client(discovery_client)

    def __start_continuous_discovery_thread(self):
        self._discovery_thread = Thread(target=self._continuous_discovery, daemon=True)
        self._discovery_thread.name = 'discovery-' + self.application_id
        self._discovery_thread.setDaemon(True)
        self._discovery_thread.start()

    def wait_for_discovery_result(self) -> None:
        while not self.discovery_result:
            if self._initialization_exception:
                raise self._initialization_exception
            logger.info('Waiting for Discovery Result.')
            sleep(BACKOFF_PERIOD)

    def register_discovery_client(self, client):
        if len(self.discovery_clients) == 0:
            self._execute_discovery_request()
        self.discovery_clients.append(client)
        if self.discovery_result:
            client.on_discovery_properties_changed(self.discovery_result)

    def deregister_discovery_client(self, client):
        self.discovery_clients.remove(client)

    def _continuous_discovery(self) -> None:
        while not self.stop_discovery:
            if len(self.discovery_clients) != 0:
                self._execute_discovery_request()
            if not self.discovery_result or not self.discovery_result[BOOTSTRAP_SERVERS_KEY]:
                sleep(BACKOFF_PERIOD)
            else:
                sleep(int(self.discovery_result[TTL_KEY]) / 1000)

    def _create_headers(self) -> dict:
        return {
            'X-Application-Id': self.application_id,
            'X-Application-Version': self.application_version,
            'X-Client-Library': 'axual-python-client',
            'X-Client-Library-Version': __version__
        }

    def _create_params(self) -> dict:
        return {
            'applicationId': self.application_id,
            'tenant': self.tenant,
            'env': self.environment
        }

    def _execute_discovery_request(self) -> None:
        latest_properties = {}
        try:
            response = requests.get(url=self.endpoint,
                                    headers=self._create_headers(),
                                    params=self._create_params(),
                                    verify=self.root_ca_location,
                                    cert=(self.ssl_certificate_location, self.ssl_key_location),
                                    timeout=5)
            if response.ok:
                latest_properties = json.loads(response.content)
                latest_properties[TIMESTAMP_KEY] = datetime.utcnow()
                self._initialization_exception = None
            else:
                self._handle_non_200(response)
        except Exception as e:
            logger.error(f'Could not fetch Discovery API result: {e}')
            self._stop_if_not_initialized(e)
        self._process_discovery_result(latest_properties)

    def _handle_non_200(self, response) -> None:
        if response.status_code == 204:
            # Backoff should be triggered
            logger.warning('Empty response from Discovery API, no active clusters found')
            self._stop_if_not_initialized(NoClusterAvailableException)
        elif response.status_code == 403:
            logger.warning('Forbidden to query Discovery API')
            self._stop_if_not_initialized(NoClusterAvailableException)
        elif response.status_code == 503:
            logger.warning('Discovery API unavailable')
            self._stop_if_not_initialized(RequestException)
        else:
            msg = f'Unexpected response code from Discovery API: {response.status_code}'
            logger.warning(msg)
            self._stop_if_not_initialized(RequestException)

    def _stop_if_not_initialized(self, exception_type):
        if not self.initialized:
            self.stop_discovery = True
            self._initialization_exception = exception_type

    def _is_cluster_change_detected(self, discovery_result: dict) -> bool:
        new_bootstrap = discovery_result.get(BOOTSTRAP_SERVERS_KEY)
        return (not self.discovery_result and discovery_result) \
            or self.discovery_result.get(BOOTSTRAP_SERVERS_KEY) != new_bootstrap

    def _process_discovery_result(self, latest_discovery_result: dict) -> None:
        if latest_discovery_result and self._is_cluster_change_detected(latest_discovery_result):
            logger.debug(f'Discovery result changed to: {dict_to_str(latest_discovery_result)}')
            for client in self.discovery_clients:
                client.on_discovery_properties_changed(latest_discovery_result)
            self.discovery_result = latest_discovery_result
            self.initialized = True

    @staticmethod
    def set_backoff_period(backoff_period: int):
        global BACKOFF_PERIOD
        BACKOFF_PERIOD = backoff_period


class DiscoveryClientRegistry:
    discovery_clients = {}

    @classmethod
    def register_client(cls,
                        config: dict,
                        discovery_client: DiscoveryClient) -> DiscoveryFetcher:
        app_id = config['application_id']
        if app_id not in cls.discovery_clients:
            fetcher = DiscoveryFetcher(config, discovery_client)
            cls.discovery_clients[app_id] = fetcher
        else:
            cls.discovery_clients[app_id].register_discovery_client(discovery_client)
        return cls.discovery_clients[app_id]

    @classmethod
    def deregister_client(cls,
                          application_id: str,
                          discovery_client: DiscoveryClient) -> None:
        if application_id in cls.discovery_clients:
            cls.discovery_clients[application_id]\
                .deregister_discovery_client(discovery_client)
