Axual Python Client
-------------------

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pipeline Status](https://gitlab.com/axual-public/axual-client-python/badges/master/pipeline.svg)](https://gitlab.com/axual-public/axual-client-python/commits/master) 
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=axual-public-axual-client-python&metric=alert_status&token=803308122363db3988c6a86bfedcb42d5b4a6791)](https://sonarcloud.io/dashboard?id=axual-public-axual-client-python)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=axual-public-axual-client-python&metric=sqale_rating&token=803308122363db3988c6a86bfedcb42d5b4a6791)](https://sonarcloud.io/dashboard?id=axual-public-axual-client-python)

Python client library that enables interaction with the Axual platform.

![Python Client Overview](http://www.plantuml.com/plantuml/png/VP0zQyCm48Rdw5TSJI6J6-hP14AxT0jqB1s4T8v5zA7ALca8_Uzrpht4zf39kkTz_HpSW_7APerGAnkoDhupXxRV76Lpb5iXrc8DAaI36eotnYEqc12Q51pqBKAqqlVPsGqqmMfCJyCVeadI8HJx57HMc436M83i838uYvKABWQFleTYzvEb1MNDC5rxuoX-MVOIV9VTHAO8t9TnxofZ6xKebjG_YvdarNGgV6CwmMx_HZLz8RFEkshHIKXuC5sVJjJYGQo-CcQ4eduS3qafFP_lP9KGAre4vKThj4R_MMudKdxDOhQENoWPLV-eWlBMkfpWTbseXuGMBY5lMd3MS4niSc1oBI4z5uhg3m00)

## Prerequisites

Python 3 is required, Python 3.6 or greater is recommended.

## Installation

```bash
pip install axual-client-python
```

## Testing
Tests are located in the `tests/` directory.
To run all of them:
```bash
python -m unittest discover tests
```

## Usage
### Producer

```python
import json
from axualclient.producer import Producer

conf = {
    # Axual configuration
    'application_id': application_id,
    'endpoint': endpoint,
    'tenant': tenant,
    'environment': environment,
    # SSL configuration
    'ssl.certificate.location': producer_app_cert,
    'ssl.key.location': producer_app_key,
    'ssl.ca.location': root_cert,
}
producer = Producer(conf)
producer.produce(value=json.dumps(dict(a=1, b='banana')))
producer.flush()  # Flushes producer before ending (triggering callbacks for delivery reports)
```
See [SSL Configuration](#ssl-configuration) for more info on the certificates required.

### Consumer

```python
from axualclient.consumer import Consumer

conf = {
    # Axual configuration
    'application_id': application_id,
    'endpoint': endpoint,
    'tenant': tenant,
    'environment': environment,
    # SSL configuration
    'ssl.certificate.location': producer_app_cert,
    'ssl.key.location': producer_app_key,
    'ssl.ca.location': root_cert,
    # Consumer configuration
    'auto.offset.reset': 'earliest',
    'on_commit': on_commit_callback,
}
consumer = Consumer(conf)

try:
    # Subscribe to topic(s) as they appear on Self Service
    consumer.subscribe(['your-topic'])
    while True:
        msg = consumer.poll(1.0)

        # msg is None if no new message
        if msg is None:
            continue

        if msg.error():
            # Error handling
            raise KafkaException(msg.error())
        else:
            # Do some processing on the message
            print(
                f'Received message on topic {msg.topic()} partition {msg.partition()} '
                f'offset {msg.offset()} key {msg.key()} value {msg.value()}'
            )
            # Commit message offset to the topic
            consumer.commit()
finally:
    if consumer is not None:
        # Cleanly unregister from cluster by closing consumer
        consumer.commit()
        consumer.close()
```

### Producer (AVRO)
Producing AVRO messages works if you have the AVRO schema available that was uploaded to self-service. 
Those schemas need to be provided to the serializer via the `schema_str` as Avro [Schema Declaration](https://avro.apache.org/docs/current/spec.html#schemas>).
```python
from axualclient.avro import AvroSerializer
from axualclient.serializing_producer import SerializingProducer

key_serializer = AvroSerializer(schema_str=Application.SCHEMA, to_dict=application_to_dict)
value_serializer = AvroSerializer(schema_str=ApplicationLogEvent.SCHEMA, to_dict=application_log_event_to_dict)

conf = {
    # Axual configuration
    'application_id': application_id,
    'endpoint': endpoint,
    'tenant': tenant,
    'environment': environment,
    # SSL configuration
    'ssl.certificate.location': producer_app_cert,
    'ssl.key.location': producer_app_key,
    'ssl.ca.location': root_cert,
    # Producer configuration
    'key.serializer': key_serializer,
    'value.serializer': value_serializer,
    'acks': 'all',
}
producer = SerializingProducer(conf)

producer.produce(topic=topic, value=value, key=key)
producer.flush() # Flushes producer before ending (triggering callbacks for delivery reports)
```

### Consumer (AVRO)
Consumer `AvroDeserializers` need to be instantiated and passed as configuration to the Axual `DeserializingConsumer` like so:
```python
from axualclient.avro import AvroDeserializer
from axualclient.deserializing_consumer import DeserializingConsumer

# Initialize Deserializers:
key_deserializer = AvroDeserializer(
    # Optional parameters
    schema_str=Application.SCHEMA,
    from_dict=dict_to_application
)
value_deserializer = AvroDeserializer(
    # Optional parameters
    schema_str=ApplicationLogEvent.SCHEMA,
    from_dict=dict_to_application_log_event,
)

configuration = {
    # Axual configuration
    'application_id': application_id,
    'endpoint': endpoint,
    'tenant': tenant,
    'environment': environment,
    # SSL configuration
    'ssl.certificate.location': producer_app_cert,
    'ssl.key.location': producer_app_key,
    'ssl.ca.location': root_cert,
    # Consumer configuration
    'key.deserializer': key_deserializer,
    'value.deserializer': value_deserializer,
    'auto.offset.reset': 'earliest',
    'on_commit': on_commit_callback,
    'error_cb': on_error_callback,
    'logger': logger
}

consumer = DeserializingConsumer(configuration)

try:
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll()

        if msg is None:
            continue

        if msg.error():
            print(f'Error returned by poll: {msg.error()}')
        else:
            print(
                f'Received message on topic {msg.topic()} partition {msg.partition()} '
                f'offset {msg.offset()} key: {str(msg.key())} value: {str(msg.value())}'
            )
            consumer.commit()
except KeyboardInterrupt:
    print('Caught KeyboardInterrupt, stopping.')
finally:
    if consumer is not None:
        print('Committing final offsets and leaving group.')
        consumer.commit()
        consumer.close()
```


## SSL Configuration
The client configuration requires a correct SSL configuration in order to communicate securely with brokers, the discovery API, and the schema registry.  
Each application (as defined in self-service) requires an application certificate (`ssl.certificate.location`) and corresponding private key (`ssl.key.location`). 
The application certificate must match the one uploaded in self-service for that application.  
The file with root certificates needs to be created properly: the brokers might be using a root certificate authority different 
from the authority that signed the certificates for the discovery API and schema registry.
The base64-encoded unencrypted versions of these certificates can be pasted into one file (`ssl.ca.location`).
This file would then look like the following example:
```
-----BEGIN CERTIFICATE-----
MIIQdaGDAksKadksSDKNsdka5sjy8elAMsm3d .....
 ...  more base64-encoded content here ...
..... LKlmsf02mz2EWYnds=
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIPmsd92nNWlasHWdwMOe92nwoa2QNinnNaZ .....
 ...  more base64-encoded content here ...
..... ldFAf02SArubBW7wVFW2i1=
-----END CERTIFICATE-----
```

## Examples

Simple use cases using the client code can be found in the 
[Axual Python Client Examples](https://gitlab.com/axual-public/axual-client-python-examples).


## Known Limitations

- We have encountered issues when using `root_ca`s consisting of more than 1 intermediate certificates.
The issue originates with the underlying SSL C library implementation and results in the following exception 
when authenticating:

```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: path length constraint exceeded (_ssl.c:1123)
```
- Transaction support is not there. An [issue](https://gitlab.com/axual-public/axual-client-python/-/issues/17) is already created and transactions will be supported in future releases.
- PEM as string format is not supported. An [issue](https://gitlab.com/axual-public/axual-client-python/-/issues/19) is already created and will be added in future releases.

## Contributing

Axual is interested in building the community; we would welcome any thoughts or 
[patches](https://gitlab.com/axual-public/axual-client-python/-/issues).
You can reach us [here](https://axual.com/contact/).

See [contributing](https://gitlab.com/axual-public/axual-client-python/blob/master/CONTRIBUTING.md).

### Building locally
This project uses [poetry](https://python-poetry.org/docs/) for dependency management and building.
Install the tool as per the instructions on the linked page, and build the library using:

    poetry build

#### For maintainers: building a release
The version of the library being built will be the version specified in `pyproject.toml` whenever you 
push to a branch. 
<br>
When tagging and building a release however, please be aware that the CI pipeline will ignore the version in `pyproject.toml` and 
build a release based on what is specified in the tag; 
for example tagging `1.0.0-alpha4` will produce `axual_client_python-1.0.0a4-py3-none-any.whl`.
<p>
This has two consequences:

- You have to follow the normal [semver](https://semver.org/) rules when choosing a tag
- After releasing, it falls on the developer to manually update the version in `pyproject.toml` in preparation for the next version.


## License

Axual Python Client is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).