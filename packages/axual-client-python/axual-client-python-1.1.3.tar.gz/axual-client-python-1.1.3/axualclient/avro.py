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
import confluent_kafka.schema_registry.avro
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer as KafkaAvroDeserializer
from confluent_kafka.schema_registry.avro import AvroSerializer as KafkaAvroSerializer
from confluent_kafka.serialization import SerializationContext

from axualclient.util import is_documented_by


class AvroSerializer(KafkaAvroSerializer):
    """ Configured on cluster detection/switch """

    def __init__(self,
                 schema_str: str,
                 to_dict: callable = None,
                 conf: dict = None
                 ):
        """
        @param schema_str (str): Avro `Schema Declaration. <https://avro.apache.org/docs/current/spec.html#schemas>`_
               If not provided, writer schema is used for deserialization.
        @param to_dict (callable, optional): Callable(object, SerializationContext) -> dict. Converts object to a dict.
        @param conf (dict): AvroSerializer configuration.
        """
        self._serializer = None
        self.schema_str = schema_str
        self.to_dict = to_dict
        self.conf = conf

        if self.conf is None:
            self.conf = {}
        self.conf['auto.register.schemas'] = False

    @is_documented_by(confluent_kafka.schema_registry.avro.AvroSerializer.__call__)
    def __call__(self, value: bytes, ctx: SerializationContext) -> bytes:
        if not self._serializer:
            raise RuntimeError('AvroSerializer is not configured')
        return self._serializer.__call__(value, ctx)

    def configure(self, configuration: dict) -> None:
        """
        Create the AvroSerializer against the newly acquired SchemaRegistry url
        @param configuration: configuration to instantiate SchemaRegistryClient
        @return: None
        """
        schema_registry_client = SchemaRegistryClient(configuration)
        self._serializer = KafkaAvroSerializer(
            schema_registry_client=schema_registry_client,
            schema_str=self.schema_str,
            to_dict=self.to_dict,
            conf=self.conf
        )


class AvroDeserializer(KafkaAvroDeserializer):
    """ Configured on cluster detection/switch """

    def __init__(self,
                 schema_str: str = None,
                 from_dict: callable = None,
                 return_record_name: bool = False
                 ):
        """
        @param schema_str str (optional):  Avro reader schema declaration.
               If not provided, writer schema is used for deserialization.
        @param from_dict callable (optional):  Converts object literal(dict) to an instance of some object.
               must be callable with the signature: from_dict(SerializationContext, dict) -> object
        @param return_record_name (bool): If True, when reading a union of records, the result will
               be a tuple where the first value is the name of the record and the second value is
               the record itself.  Defaults to False.
        """
        self._deserializer = None
        self.schema_str = schema_str
        self.from_dict = from_dict
        self.return_record_name = return_record_name

    @is_documented_by(confluent_kafka.schema_registry.avro.AvroDeserializer.__call__)
    def __call__(self, value: bytes, ctx: SerializationContext) -> bytes:
        if not self._deserializer:
            raise RuntimeError('AvroDeserializer is not configured')
        return self._deserializer.__call__(value, ctx)

    def configure(self, configuration: dict) -> None:
        """
        Create the AvroDeserializer against the newly acquired SchemaRegistry url
        @param configuration: configuration to instantiate SchemaRegistryClient
        @return: None
        """
        schema_registry_client = SchemaRegistryClient(configuration)
        self._deserializer = KafkaAvroDeserializer(
            schema_registry_client=schema_registry_client,
            from_dict=self.from_dict,
            return_record_name=self.return_record_name
        )
