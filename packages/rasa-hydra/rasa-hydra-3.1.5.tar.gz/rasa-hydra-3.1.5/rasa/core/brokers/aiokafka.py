import json
import logging
import asyncio
from typing import Optional

from rasa.core.brokers.event_channel import EventChannel
from rasa.utils.io import DEFAULT_ENCODING
from aiokafka.producer.producer import AIOKafkaProducer
from aiokafka.helpers import create_ssl_context
from aiokafka.errors import KafkaError, KafkaTimeoutError

logger = logging.getLogger(__name__)


class AIOKafkaMiddleware(EventChannel):
    def __init__(
        self,
        host,
        sasl_username=None,
        sasl_password=None,
        ssl_cafile=None,
        ssl_certfile=None,
        ssl_keyfile=None,
        ssl_check_hostname=False,
        topic="rasa_core_events",
        security_protocol="SASL_PLAINTEXT",
        loglevel=logging.ERROR,
    ):
        if host and ',' in host:
            self.host = host.split(",")
        else:
            self.host = host
        self.topic = topic
        self.security_protocol = security_protocol
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.ssl_cafile = ssl_cafile
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        self.ssl_check_hostname = ssl_check_hostname
        self.is_healthy = True
        self.producer = self._create_producer()
        logger.info("Starting AIOKafka health check.")
        asyncio.get_event_loop().create_task(self.is_connected())

        logging.getLogger("kafka").setLevel(loglevel)

    @classmethod
    def from_endpoint_config(cls, broker_config) -> Optional["AIOKafkaMiddleware"]:
        if broker_config is None:
            return None

        return cls(broker_config.url, **broker_config.kwargs)
    
    async def is_connected(self):
        await asyncio.sleep(5)
        random_node_id = self.producer.client.get_random_node()
        while True:
            try:
                self.is_healthy = await self.producer.client.ready(random_node_id)
            except Exception as exp:
                self.is_healthy = False
                logger.error(f"AIOKafkaProducer client is unable to connect to the Kafka cluster. {exp}")
            await asyncio.sleep(10)

    async def publish(self, event):
        await self._publish(event)
    
    async def flush(self):
        await self.producer.flush()

    def _create_producer(self):
        if self.security_protocol == "SASL_PLAINTEXT":
            producer = AIOKafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                sasl_plain_username=self.sasl_username,
                sasl_plain_password=self.sasl_password,
                sasl_mechanism="PLAIN",
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "SSL":
            producer = AIOKafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                ssl_context=create_ssl_context(
                    cafile=self.ssl_cafile,
                    certfile=self.ssl_certfile,
                    keyfile=self.ssl_keyfile
                ),
                security_protocol=self.security_protocol,
            )
        elif self.security_protocol == "PLAINTEXT":
            producer = AIOKafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        else:
            producer = None
        asyncio.get_event_loop().create_task(producer.start())
        return producer

    async def _publish(self, event):
        try:
            if event.get('sender_id'):
                await self.producer.send(self.topic, value=event, key=bytes(event.get('sender_id'), 'utf-8'))
            else:
                await self.producer.send(self.topic, event)
        except KafkaTimeoutError:
            logger.error("Producing to topic timed out.")
        except KafkaError as err:
            logger.error("Producing caused a Kafka error: {}".format(err))

    def _close(self):
        self.producer.stop()

