# -*- coding: utf-8 -*-
#
#      Copyright (C) 2022 Axual B.V.
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

import logging
import threading
from abc import abstractmethod
from time import sleep
from typing import Callable
from typing import List

import confluent_kafka
from confluent_kafka import TopicPartition
from confluent_kafka.admin import ClusterMetadata

from axualclient.discovery import DiscoveryClientRegistry, DiscoveryClient, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY
from axualclient.patterns import resolve_topic, resolve_topic_partitions, \
    unresolve_topics_in_cluster_metadata
from axualclient.util import calculate_producer_switch_timeout, is_documented_by

logger = logging.getLogger(__name__)


class _AxualProducer(DiscoveryClient):
    """
    Super class for Axual producers (String, AVRO) implementing common producers' logic.
    Not intended to be directly instantiated.
    """

    @abstractmethod
    def on_discovery_properties_changed(self,
                                        discovery_result: dict):
        pass

    def __init__(self,
                 configuration: dict,
                 *args, **kwargs):
        """
        Instantiate a producer for Axual. The _producer attribute is the confluent_kafka Producer class.

        Parameters
        ----------
        configuration : dict
            Configuration properties including Axual Configuration. All producer Configuration can be found at:
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Producer.
        """
        self._producer = None  # no discovery result yet

        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = configuration
        # bootstrap servers & key/value serializers are not available at this point yet
        self.configuration['security.protocol'] = 'SSL'
        if 'partitioner' not in self.configuration.keys():
            self.configuration['partitioner'] = 'murmur2_random'

        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

        self.discovery_result = {}
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            self.configuration, self
        )

    def _switch_producer(self, discovery_result, producer):
        if self._producer is not None:
            self._producer.flush()
            switch_timeout = calculate_producer_switch_timeout(
                self._is_keeping_order(),
                int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]),
                int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]),
                discovery_result[TIMESTAMP_KEY]
            )
            sleep(switch_timeout)

        self._producer = producer

    def wait_for_initialization(self) -> None:
        if self._producer is not None:
            return
        with self.init_lock:
            self.discovery_fetcher.wait_for_discovery_result()

    def _do_with_switch_lock(self, func):
        self.wait_for_initialization()
        with self.switch_lock:
            return func()

    def _get_producer(self):
        """ Convenience method added such that lambda expressions do not get evaluated on the old proxied object """
        return self._producer

    def _is_keeping_order(self):
        return self.configuration.get('max.in.flight.requests.per.connection') in [1, '1']

    @is_documented_by(confluent_kafka.cimpl.Producer.produce)
    def produce(self,
                topic: str,
                value=None,
                key=None,
                partition: int = None,
                on_delivery: Callable = None,
                timestamp: int = None,
                headers: dict = None,
                *args, **kwargs) -> None:
        if value is not None:
            kwargs['value'] = value
        if key is not None:
            kwargs['key'] = key
        if partition is not None:
            kwargs['partition'] = partition
        if on_delivery is not None:
            kwargs['on_delivery'] = on_delivery
        if timestamp is not None:
            kwargs['timestamp'] = timestamp
        if headers is not None:
            kwargs['headers'] = headers
        self._do_with_switch_lock(
            lambda:
            self._get_producer().produce(resolve_topic(self.discovery_result, topic), *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.abort_transaction)
    def abort_transaction(self, timeout: float = None, *args, **kwargs):
        if timeout is not None:
            self._do_with_switch_lock(
                lambda: self._get_producer().abort_transaction(timeout, *args, **kwargs)
            )
        else:
            self._do_with_switch_lock(
                lambda: self._get_producer().abort_transaction(*args, **kwargs)
            )

    @is_documented_by(confluent_kafka.cimpl.Producer.begin_transaction)
    def begin_transaction(self, *args, **kwargs):
        self._do_with_switch_lock(
            lambda: self._get_producer().begin_transaction(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.commit_transaction)
    def commit_transaction(self, timeout: float = None, *args, **kwargs):
        if timeout is not None:
            self._do_with_switch_lock(
                lambda: self._get_producer().commit_transaction(timeout, *args, **kwargs)
            )
        else:
            self._do_with_switch_lock(
                lambda: self._get_producer().commit_transaction(*args, **kwargs)
            )

    @is_documented_by(confluent_kafka.cimpl.Producer.flush)
    def flush(self, timeout: float = None, *args, **kwargs) -> int:
        if timeout is None:
            return self._do_with_switch_lock(
                lambda: self._get_producer().flush(*args, **kwargs)
            )
        return self._do_with_switch_lock(
            lambda: self._get_producer().flush(timeout, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.init_transactions)
    def init_transactions(self, timeout: float, *args, **kwargs) -> None:
        self._do_with_switch_lock(
            lambda: self._get_producer().init_transactions(timeout, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.list_topics)
    def list_topics(self,
                    topic: str = None,
                    timeout: float = -1,
                    *args, **kwargs) -> ClusterMetadata:
        resolved_topic = resolve_topic(self.discovery_result, topic)

        cluster_metadata = self._do_with_switch_lock(
            lambda: self._get_producer().list_topics(resolved_topic, timeout, *args, **kwargs)
        )

        converted_topics = unresolve_topics_in_cluster_metadata(self.discovery_result, cluster_metadata)
        cluster_metadata.topics = converted_topics
        return cluster_metadata

    @is_documented_by(confluent_kafka.cimpl.Producer.poll)
    def poll(self, timeout=None, *args, **kwargs):
        if timeout is not None:
            kwargs['timeout'] = timeout
        return self._do_with_switch_lock(
            lambda: self._get_producer().poll(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.purge)
    def purge(self, in_queue: bool = True, in_flight: bool = True, blocking: bool = True, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_producer().purge(in_queue, in_flight, blocking, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Producer.send_offsets_to_transaction)
    def send_offsets_to_transaction(self,
                                    offsets: List[TopicPartition],
                                    group_metadata: object,
                                    timeout=None,
                                    *args, **kwargs):
        if timeout is not None:
            kwargs['timeout'] = timeout

        resolved_partitions = resolve_topic_partitions(self.discovery_result, offsets)

        self._do_with_switch_lock(
            lambda: self._get_producer().send_offsets_to_transaction(
                resolved_partitions, group_metadata, *args, **kwargs)
        )

    def __class__(self, *args, **kwargs):
        return self._producer.__class__(*args, **kwargs)

    def __dir__(self, *args, **kwargs):
        return self._producer.__dir__(*args, **kwargs)

    def __doc__(self, *args, **kwargs):
        return self._producer.__doc__(*args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._producer.__eq__(*args, **kwargs)

    def __format__(self, *args, **kwargs):
        return self._producer.__format__(*args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._producer.__ge__(*args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._producer.__gt__(*args, **kwargs)

    def __hash__(self, *args, **kwargs):
        return self._producer.__hash__(*args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._producer.__le__(*args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._producer.__len__(*args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._producer.__lt__(*args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._producer.__ne__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self._producer.__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self._producer.__reduce_ex__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._producer.__repr__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self._producer.__sizeof__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self._producer.__str__(*args, **kwargs)
