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
import logging

from confluent_kafka import Consumer as KafkaConsumer

from axualclient.axual_consumer import _AxualConsumer
from axualclient.discovery import BOOTSTRAP_SERVERS_KEY
from axualclient.patterns import resolve_group
from axualclient.util import filter_axual_configuration

logger = logging.getLogger(__name__)


class Consumer(_AxualConsumer):
    """Simple consumer class.
    """

    def __init__(self,
                 configuration: dict = None,
                 *args, **kwargs):
        """
        Instantiate a consumer for Axual. Derives from confluent_kafka
         Consumer class.
        Note that auto-commit is set to False, so received messages must
         be committed by your script's logic.

        Parameters
        ----------
        configuration: dict
            Configuration properties including Axual Configurations. All consumer Configurations can be found at:
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs:
            Other parameters that can be passed to confluent_kafka Consumer.
        """
        super().__init__(configuration, *args, **kwargs)

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            self.discovery_result = discovery_result
            # plug in the new bootstrap servers
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]
            # plug in the resolved group.id
            self.configuration['group.id'] = resolve_group(discovery_result, self.unresolved_group_id)
            logger.debug(f'group.id: {self.configuration["group.id"]}')

            # Switch consumer
            kafka_properties = filter_axual_configuration(self.configuration)
            consumer = KafkaConsumer(kafka_properties, *self.init_args, **self.init_kwargs)
            self._switch_consumer(discovery_result, consumer)
