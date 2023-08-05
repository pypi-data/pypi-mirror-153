# -*- coding: utf-8 -*-
#
#      Copyright (C) 2021 Axual B.V.
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
from typing import Optional, List

from confluent_kafka import TopicPartition
from confluent_kafka.admin import ClusterMetadata

GROUP_PLACEHOLDER = '{group}'
ENVIRONMENT_PLACEHOLDER = '{environment}'
INSTANCE_PLACEHOLDER = '{instance}'
TENANT_PLACEHOLDER = '{tenant}'
TOPIC_PLACEHOLDER = '{topic}'

# Move those on another class maybe
GROUP_KEY = 'group'
ENVIRONMENT_KEY = 'environment'
INSTANCE_KEY = 'instance'
TENANT_KEY = 'tenant'
TOPIC_KEY = 'topic'
TOPIC_PATTERN_KEY = 'topic.pattern'
GROUP_PATTERN_KEY = 'group.id.pattern'

logger = logging.getLogger(__name__)


def resolve_topic(discovery_result: dict, topic: Optional[str]) -> Optional[str]:
    if topic is None:
        return
    return discovery_result[TOPIC_PATTERN_KEY] \
        .replace(TENANT_PLACEHOLDER, discovery_result[TENANT_KEY]) \
        .replace(INSTANCE_PLACEHOLDER, discovery_result[INSTANCE_KEY]) \
        .replace(ENVIRONMENT_PLACEHOLDER, discovery_result[ENVIRONMENT_KEY]) \
        .replace(TOPIC_PLACEHOLDER, topic)


def resolve_topics(discovery_result: dict, topics: Optional[list]) -> Optional[List[str]]:
    if not topics:
        return None
    return [resolve_topic(discovery_result, t) for t in topics]


def unresolve_topic(discovery_result: dict, topic: str) -> Optional[str]:
    if topic is not None and topic.startswith('_'):
        return topic

    if topic is None or not __is_topic_in_the_pattern_format(discovery_result, topic):
        logger.warning('Provided topic [' + str(topic) + '] is not in the format described by topic pattern ['
                       + discovery_result[TOPIC_PATTERN_KEY] + '].')
        return topic

    unresolved_topic = topic.replace(discovery_result[TENANT_KEY] + '-', '') \
        .replace(discovery_result[INSTANCE_KEY] + '-', '') \
        .replace(discovery_result[ENVIRONMENT_KEY] + '-', '')

    if len(unresolved_topic) > 0 and unresolved_topic != discovery_result[ENVIRONMENT_KEY]:
        return unresolved_topic

    return topic


def unresolve_topics(discovery_result: dict, topics: Optional[list]) -> Optional[List[str]]:
    return [unresolve_topic(discovery_result, topic) for topic in topics]


def unresolve_topics_in_cluster_metadata(discovery_result: dict, cluster_metadata: ClusterMetadata):
    converted_topics = {}
    for key in cluster_metadata.topics.keys():
        current_entry = cluster_metadata.topics.get(key)
        converted_topic = unresolve_topic(discovery_result, current_entry.topic)
        converted_topics[converted_topic] = current_entry
        converted_topics.get(converted_topic).topic = converted_topic
    return converted_topics


def __is_topic_in_the_pattern_format(discovery_result, topic: str):
    correct_format = True

    if 'tenant' in discovery_result[TOPIC_PATTERN_KEY]:
        correct_format = discovery_result[TENANT_KEY] in topic

    if correct_format and 'instance' in discovery_result[TOPIC_PATTERN_KEY]:
        correct_format = discovery_result[INSTANCE_KEY] in topic

    if correct_format and 'environment' in discovery_result[TOPIC_PATTERN_KEY]:
        correct_format = discovery_result[ENVIRONMENT_KEY] in topic

    return correct_format


def resolve_topic_partition(discovery_result: dict, partition: TopicPartition) -> Optional[TopicPartition]:
    if partition is None:
        return None
    return TopicPartition(resolve_topic(discovery_result, partition.topic), partition.partition, partition.offset)


def resolve_topic_partitions(discovery_result: dict, partitions: List[TopicPartition]) -> Optional[List[TopicPartition]]:
    if not partitions:
        return None
    return [resolve_topic_partition(discovery_result, topic_partition) for topic_partition in partitions]


def unresolve_topic_partition(discovery_result: dict, partition: TopicPartition) -> Optional[TopicPartition]:
    if partition is None:
        return None
    return TopicPartition(unresolve_topic(discovery_result, partition.topic), partition.partition, partition.offset)


def unresolve_topic_partitions \
                (discovery_result: dict, partitions: List[TopicPartition]) -> Optional[List[TopicPartition]]:
    if not partitions:
        return None
    return [unresolve_topic_partition(discovery_result, topic_partition) for topic_partition in partitions]


def resolve_group(discovery_result: dict, group: Optional[str]) -> Optional[str]:
    if group is None:
        return
    return discovery_result[GROUP_PATTERN_KEY] \
        .replace(TENANT_PLACEHOLDER, discovery_result[TENANT_KEY]) \
        .replace(INSTANCE_PLACEHOLDER, discovery_result[INSTANCE_KEY]) \
        .replace(ENVIRONMENT_PLACEHOLDER, discovery_result[ENVIRONMENT_KEY]) \
        .replace(GROUP_PLACEHOLDER, group)
