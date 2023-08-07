import logging
import time
from typing import Any, Generator

from kafka import KafkaConsumer, errors
from kafka.consumer.fetcher import ConsumerRecord

from core.backoff import backoff


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaExtractor:
    def __init__(self, kafka_consumer: KafkaConsumer) -> None:
        self.consumer = kafka_consumer

    def _commit(self):
        self.consumer.commit()

    def extract(self) -> Generator[ConsumerRecord, None, None]:
        """Метод для чтения сообщений из Kafka."""
        try:
            yield from self.consumer
        except errors.KafkaError as e:
            logger.error("Error while reading messages from Kafka: %s", e)
        except Exception as e:
            logger.error("Error while reading messages from Kafka: %s", e)


@backoff()
def get_kafka_extractor(settings: dict[str, Any]):
    consumer = KafkaConsumer(
        settings["topic"],
        bootstrap_servers=settings["bootstrap_servers"],
        auto_offset_reset=settings["auto_offset_reset"],
        group_id=settings["group_id"],
        enable_auto_commit=False,
        consumer_timeout_ms=1000,
    )
    return KafkaExtractor(consumer)
