"""Kafka broker for the persistence worker."""

from faststream.kafka import KafkaBroker

from trakr_core.config import get_settings

# FastStream 0.7 has no broker-wide consumer group. Subscribers should pass this.
CONSUMER_GROUP_ID = "trakr-persistence-worker"

settings = get_settings()

broker = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)
