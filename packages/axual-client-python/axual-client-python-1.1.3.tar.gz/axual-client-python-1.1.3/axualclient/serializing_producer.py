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

from confluent_kafka import SerializingProducer as KafkaSerializingProducer
from confluent_kafka.serialization import Serializer

from axualclient.avro import AvroSerializer
from axualclient.axual_producer import _AxualProducer
from axualclient.discovery import BOOTSTRAP_SERVERS_KEY, SCHEMA_REGISTRY_URL_KEY
from axualclient.util import first_of_string_list, filter_axual_configuration

logger = logging.getLogger(__name__)


class SerializingProducer(_AxualProducer):

    def __init__(self,
                 configuration: dict,
                 *args, **kwargs):
        """
        Instantiate an AVRO producer for Axual. The _producer attribute is
         the confluent_kafka SerializingProducer class.

        Parameters
        ----------
        configuration: dict
            App config information
        *args and **kwargs:
            Other parameters that can be passed to confluent_kafka Producer.

        """
        super().__init__(configuration, *args, **kwargs)

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            self.discovery_result = discovery_result
            # plug in the new bootstrap servers
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]

            # initialize serializers against new schema registry
            sr_url = first_of_string_list(discovery_result[SCHEMA_REGISTRY_URL_KEY])

            self._reconfigure_serializer(self.configuration['key.serializer'], sr_url)
            self._reconfigure_serializer(self.configuration['value.serializer'], sr_url)

            # Switch producer
            kafka_properties = filter_axual_configuration(self.configuration)
            producer = KafkaSerializingProducer(kafka_properties, *self.init_args, **self.init_kwargs)
            self._switch_producer(discovery_result, producer)

    def _reconfigure_serializer(self, serializer: Serializer, schema_registry_url: str) -> None:
        """
        AvroSerializers need to be reconfigured with the new target SchemaRegistry.
        @param serializer: the serializer to reconfigure
        @param schema_registry_url: the new SchemaRegistry url
        @return: None
        """
        if isinstance(serializer, AvroSerializer):
            serializer.configure({
                'url': schema_registry_url,
                'ssl.ca.location': self.configuration['ssl.ca.location'],
                'ssl.key.location': self.configuration['ssl.key.location'],
                'ssl.certificate.location': self.configuration['ssl.certificate.location']
            })

    def __class__(self, *args, **kwargs):
        return self._producer.__class__(*args, **kwargs)

    def __dir__(self, *args, **kwargs):
        return self._producer.__dir__(*args, **kwargs)

    def __doc__(self, *args, **kwargs):
        return self._producer.__doc__(*args, **kwargs)
