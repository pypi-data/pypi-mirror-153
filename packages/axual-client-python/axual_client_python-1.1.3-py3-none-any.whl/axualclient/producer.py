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

from confluent_kafka import Producer as KafkaProducer

from axualclient.axual_producer import _AxualProducer
from axualclient.discovery import BOOTSTRAP_SERVERS_KEY
from axualclient.util import filter_axual_configuration

logger = logging.getLogger(__name__)


class Producer(_AxualProducer):

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
        super().__init__(configuration, *args, **kwargs)

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            self.discovery_result = discovery_result
            # plug in the new bootstrap servers
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]

            # Switch producer
            kafka_properties = filter_axual_configuration(self.configuration)
            producer = KafkaProducer(kafka_properties, *self.init_args, **self.init_kwargs)
            self._switch_producer(discovery_result, producer)
