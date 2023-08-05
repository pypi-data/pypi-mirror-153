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
from datetime import datetime
from time import sleep
from typing import List, Tuple, Callable

import confluent_kafka
from confluent_kafka import TopicPartition, Message
from confluent_kafka.admin import ClusterMetadata

from axualclient.discovery import DiscoveryClient, DiscoveryClientRegistry, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY, TTL_KEY
from axualclient.patterns import resolve_topics, resolve_topic_partitions, \
    unresolve_topic_partitions, resolve_topic_partition, resolve_topic, unresolve_topics_in_cluster_metadata
from axualclient.util import is_documented_by

logger = logging.getLogger(__name__)

DEFAULT_POLL_SPEED = 0.2


class _AxualConsumer(DiscoveryClient):
    """
    Super class for Axual consumers (String, AVRO) implementing common consumers' logic.
    Set poll_speed attribute to change the polling speed (default: 0.2 [secs]).
    Not intended to be directly instantiated.
    """

    @abstractmethod
    def on_discovery_properties_changed(self, discovery_result: dict):
        pass

    def __init__(self,
                 configuration: dict = None,
                 *args, **kwargs):
        self.unresolved_topics = []
        self.unresolved_group_id = configuration.get('application_id')
        self._consumer = None
        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = configuration
        # bootstrap servers & key/value serializers are not available at this point yet
        self.configuration['security.protocol'] = 'SSL'

        self.poll_speed = DEFAULT_POLL_SPEED
        self.initialized = False
        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

        self.discovery_result = {}
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            self.configuration, self
        )

    def _switch_consumer(self, discovery_result, consumer):
        if self.initialized:
            assignment = self._consumer.assignment()
            self._consumer.close()

            # Calculate switch time-out
            if len(assignment) > 0:
                switch_timeout = self._calculate_switch_timeout(discovery_result)
                sleep(switch_timeout / 1000)

        self._consumer = consumer
        # subscribe to previously subscribed-to topics, on new cluster
        if self.unresolved_topics:
            resolved_topics = resolve_topics(self.discovery_result, self.unresolved_topics)
            self._consumer.subscribe(resolved_topics)
        self.initialized = True

    def wait_for_initialization(self) -> None:
        if self.initialized:
            return
        with self.init_lock:
            self.discovery_fetcher.wait_for_discovery_result()

    def _do_with_switch_lock(self, func):
        self.wait_for_initialization()
        with self.switch_lock:
            return func()

    def _get_consumer(self):
        """ Convenience method added such that lambda expressions do not get evaluated on the old proxied object """
        return self._consumer

    def _calculate_switch_timeout(self, discovery_result: dict):
        if self._is_at_least_once():
            return 0
        return max(int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]) *
                   int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]) -
                   (datetime.utcnow() - discovery_result[TIMESTAMP_KEY]).total_seconds() * 1000,
                   int(discovery_result[TTL_KEY]))

    def _is_at_least_once(self) -> bool:
        return self.configuration.get('auto.offset.reset') in ['earliest', 'smallest', 'begin', 'start']

    def __iter__(self):
        """Continuously loop through messages until self.pause is set to True"""
        self.pause = False
        while not self.pause:
            msg = self.poll(self.poll_speed)
            yield msg

    # KafkaConsumer interface
    @is_documented_by(confluent_kafka.cimpl.Consumer.assign)
    def assign(self, partitions: List[TopicPartition], *args, **kwargs):
        resolved_partitions = resolve_topic_partitions(self.discovery_result, partitions)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().assign(resolved_partitions, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.assignment)
    def assignment(self, *args, **kwargs) -> List[TopicPartition]:
        partitions = self._do_with_switch_lock(
            lambda: self._get_consumer().assignment(*args, **kwargs)
        )
        return unresolve_topic_partitions(self.discovery_result, partitions)

    @is_documented_by(confluent_kafka.cimpl.Consumer.close)
    def close(self, *args, **kwargs) -> None:
        DiscoveryClientRegistry.deregister_client(self.unresolved_group_id, self)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().close(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.commit)
    def commit(self,
               message: Message = None,
               offsets: List[TopicPartition] = None,
               asynchronous: bool = True,
               *args, **kwargs):
        if message is not None:
            kwargs['message'] = message
        if offsets is not None:
            kwargs['offsets'] = resolve_topic_partitions(self.discovery_result, offsets)
        kwargs['asynchronous'] = asynchronous
        return self._do_with_switch_lock(
            lambda: self._get_consumer().commit(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.committed)
    def committed(self,
                  partitions: List[TopicPartition],
                  timeout: float = None) -> List[TopicPartition]:
        resolved_partitions = resolve_topic_partitions(self.discovery_result, partitions)
        if timeout is not None:
            partitions = self._do_with_switch_lock(
                lambda: self._get_consumer().committed(resolved_partitions, timeout)
            )
        else:
            partitions = self._do_with_switch_lock(
                lambda: self._get_consumer().committed(resolved_partitions)
            )
        return unresolve_topic_partitions(self.discovery_result, partitions)

    @is_documented_by(confluent_kafka.cimpl.Consumer.consume)
    def consume(self,
                num_messages: int = 1,
                timeout: float = -1,
                *args, **kwargs) -> List[Message]:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().consume(num_messages, timeout, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.consumer_group_metadata)
    def consumer_group_metadata(self):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().consumer_group_metadata()
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.get_watermark_offsets)
    def get_watermark_offsets(self,
                              partition: TopicPartition,
                              timeout: float = None,
                              cached: bool = False,
                              *args, **kwargs) -> Tuple[int, int]:
        if timeout is not None:
            kwargs['timeout'] = timeout

        resolved_topic_partition = resolve_topic_partition(self.discovery_result, partition)

        return self._do_with_switch_lock(
            lambda: self._get_consumer().get_watermark_offsets(
                partition=resolved_topic_partition, cached=cached, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.list_topics)
    def list_topics(self,
                    topic: str = None,
                    timeout: float = -1,
                    *args, **kwargs) -> ClusterMetadata:
        resolved_topic = resolve_topic(self.discovery_result, topic)

        cluster_metadata = self._do_with_switch_lock(
            lambda: self._get_consumer().list_topics(topic=resolved_topic, timeout=timeout, *args, **kwargs)
        )

        converted_topics = unresolve_topics_in_cluster_metadata(self.discovery_result, cluster_metadata)
        cluster_metadata.topics = converted_topics
        return cluster_metadata

    @is_documented_by(confluent_kafka.cimpl.Consumer.offsets_for_times)
    def offsets_for_times(self,
                          partitions: List[TopicPartition],
                          timeout: float = None) -> List[TopicPartition]:
        resolved_partitions = resolve_topic_partitions(self.discovery_result, partitions)
        if timeout is not None:
            partitions_with_axual_topic_name = self._do_with_switch_lock(
                lambda: self._get_consumer().offsets_for_times(resolved_partitions, timeout)
            )
        else:
            partitions_with_axual_topic_name = self._do_with_switch_lock(
                lambda: self._get_consumer().offsets_for_times(resolved_partitions)
            )
        return unresolve_topic_partitions(self.discovery_result, partitions_with_axual_topic_name)

    @is_documented_by(confluent_kafka.cimpl.Consumer.pause)
    def pause(self, partitions: List[TopicPartition]) -> None:
        resolved_partitions = resolve_topic_partitions(self.discovery_result, partitions)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().pause(resolved_partitions)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.poll)
    def poll(self, timeout=None):
        if timeout is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().poll(timeout)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().poll()
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.position)
    def position(self, partitions: List[TopicPartition]) -> List[TopicPartition]:
        resolved_topic_partition = resolve_topic_partitions(self.discovery_result, partitions)

        partitions_with_axual_topic_name = self._do_with_switch_lock(
            lambda: self._get_consumer().position(resolved_topic_partition)
        )

        return unresolve_topic_partitions(self.discovery_result, partitions_with_axual_topic_name)

    @is_documented_by(confluent_kafka.cimpl.Consumer.resume)
    def resume(self, partitions: List[TopicPartition]) -> None:
        resolved_topic_partitions = resolve_topic_partitions(self.discovery_result, partitions)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().resume(resolved_topic_partitions)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.seek)
    def seek(self, partition: TopicPartition):
        resolved_topic_partition = resolve_topic_partition(self.discovery_result, partition)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().seek(resolved_topic_partition)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.store_offsets)
    def store_offsets(self,
                      message: confluent_kafka.Message = None,
                      offsets: List[TopicPartition] = None,
                      *args, **kwargs) -> None:
        if offsets is not None:
            kwargs['offsets'] = resolve_topic_partitions(self.discovery_result, offsets)
        if message is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().store_offsets(message, *args, **kwargs)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().store_offsets(*args, **kwargs)
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.subscribe)
    def subscribe(self,
                  topics: List[str],
                  on_assign: Callable = None,
                  on_revoke: Callable = None,
                  on_lost: Callable = None,
                  *args, **kwargs):
        self.unresolved_topics = list(set(self.unresolved_topics + topics))
        if on_assign is not None:
            kwargs['on_assign'] = on_assign
        if on_revoke is not None:
            kwargs['on_revoke'] = on_revoke
        if on_lost is not None:
            kwargs['on_lost'] = on_lost
        return self._do_with_switch_lock(
            lambda: self._get_consumer().subscribe(
                resolve_topics(self.discovery_result, topics), *args, **kwargs
            )
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.unassign)
    def unassign(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().unassign(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.unsubscribe)
    def unsubscribe(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().unsubscribe(*args, **kwargs)
        )
