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
from datetime import datetime

logger = logging.getLogger(__name__)


def dict_to_str(dictionary: dict) -> str:
    return json.dumps(dictionary, default=str, indent=2)


def filter_axual_configuration(configuration: dict) -> dict:
    """
    Returns a dict containing everything except for axual configuration from a dictionary
    """
    props = {}
    axual_configs = ['application_id', 'endpoint', 'environment', 'instance', 'tenant']
    for config in configuration:
        if config not in axual_configs:
            props[config] = configuration.get(config)
    return props


def first_of_string_list(comma_separated: str) -> str:
    return comma_separated.split(',')[0]


def calculate_producer_switch_timeout(is_keeping_order: bool,
                                      distributor_timeout_ms: int,
                                      distributor_distance: int,
                                      discovery_result_timestamp: datetime) -> float:
    """
    Returns the time needed for a producer to sleep prior to resuming produce operations
    @param is_keeping_order:           If not, no need to wait
    @param distributor_timeout_ms:     How long it takes for messages to distribute
    @param distributor_distance:       Defined in hops
    @param discovery_result_timestamp: When the discovery result was received
    @return: Time to sleep in seconds
    """
    if is_keeping_order:
        ms_since_discovery = max(
            (datetime.utcnow() - discovery_result_timestamp).total_seconds() * 1000,
            0
        )
        sleep_ms = distributor_timeout_ms * distributor_distance - ms_since_discovery
        return sleep_ms / 1000.
    return 0.


def is_documented_by(original: callable) -> callable:
    """
    Decorator for pointing to external documentation.
    @param original: component
    @return: callable
    """
    def wrapper(target):
        target.__doc__ = original.__doc__
        return target
    return wrapper
