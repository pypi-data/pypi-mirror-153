import json
import logging
import threading
import time
from typing import Optional

from rasa.core.brokers.event_channel import EventChannel
from rasa.utils.io import DEFAULT_ENCODING

logger = logging.getLogger(__name__)


class KafkaProducer(EventChannel):
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
        health_check_thread = threading.Thread(
            name='kafka_health_check_thread',
            target=self.is_connected,
            args=(),
            daemon=True
        )
        logger.info("Starting Kafka cluster health check thread...")
        health_check_thread.start()

        logging.getLogger("kafka").setLevel(loglevel)

    @classmethod
    def from_endpoint_config(cls, broker_config) -> Optional["KafkaProducer"]:
        if broker_config is None:
            return None

        return cls(broker_config.url, **broker_config.kwargs)

    def publish(self, event):
        # self._create_producer()
        self._publish(event)
        # self._close()

    def _create_producer(self):
        import kafka

        if self.security_protocol == "SASL_PLAINTEXT":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                sasl_plain_username=self.sasl_username,
                sasl_plain_password=self.sasl_password,
                sasl_mechanism="PLAIN",
                security_protocol=self.security_protocol,
                acks=0,
                buffer_memory=134217728,
                max_block_ms=30000
            )
        elif self.security_protocol == "SSL":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode(DEFAULT_ENCODING),
                ssl_cafile=self.ssl_cafile,
                ssl_certfile=self.ssl_certfile,
                ssl_keyfile=self.ssl_keyfile,
                ssl_check_hostname=False,
                security_protocol=self.security_protocol,
                acks=0,
                buffer_memory=134217728,
                max_block_ms=30000
            )
        elif self.security_protocol == "PLAINTEXT":
            return kafka.KafkaProducer(
                bootstrap_servers=self.host,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks=0,
                buffer_memory=134217728,
                max_block_ms=30000
            )
        else:
            return None

    def _publish(self, event):
        # self.producer.send(self.topic, event)
        try:
            if event.get('sender_id'):
                self.producer.send(self.topic, value=event, key=bytes(event.get('sender_id'), 'utf-8'))
            else:
                self.producer.send(self.topic, event)
        except Exception as exp:
            logger.error(exp)
            self.producer = self._create_producer()

    def _close(self):
        self.producer.close()

    def is_connected(self):
        while True:
            try:
                producer = self._create_producer()
                self.is_healthy = producer.bootstrap_connected()
                producer.close(timeout=5)
            except Exception as exp:
                logger.error(f"[KAFKA_CLUSTER_ERROR] - Unable to connect to Kafka cluster. {exp}")
                self.is_healthy = False
            time.sleep(10)

    def flush(self):
        self.producer.flush(30)
