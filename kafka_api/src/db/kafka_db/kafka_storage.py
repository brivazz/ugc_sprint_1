import logging
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError
from kafka.admin import KafkaAdminClient, NewTopic

import backoff
from core.config import settings
from db.kafka_db import viewing

kafka_producer: AIOKafkaProducer | None = None


@backoff.on_exception(backoff.expo, KafkaError, max_time=60)
async def on_startup(host: str, port: int):
    global kafka_producer
    kafka_producer = AIOKafkaProducer(bootstrap_servers=f"{host}:{port}")
    await kafka_producer.start()
    admin_client = KafkaAdminClient(bootstrap_servers=f"{host}:{port}")

    topic_name = settings.kafka_topic
    num_partitions = 3
    replication_factor = 1

    topic_metadata = admin_client.list_topics()
    if topic_name not in topic_metadata:
        new_topic = NewTopic(topic_name, num_partitions, replication_factor)
        admin_client.create_topics([new_topic])

    viewing.viewing_timestamp_repository = viewing.ViewingKafkaRepository(
        kafka_producer
    )


async def on_shutdown():
    await kafka_producer.stop()
