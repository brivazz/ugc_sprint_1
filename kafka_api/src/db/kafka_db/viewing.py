import logging
from uuid import UUID
import datetime
from aiokafka import AIOKafkaProducer


class ViewingKafkaRepository:
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self._producer = kafka_producer

    @staticmethod
    def get_key(film_id: UUID, user_id: UUID) -> bytes:
        key = str(user_id) + ":" + str(film_id)
        return key.encode("utf-8")

    @staticmethod
    def serialize_int(value: int) -> bytes:
        return value.to_bytes(4, "big")

    async def add_number_seconds_viewing(
        self, user_id: UUID, film_id: UUID, number_seconds_viewing: int
    ):
        kafka_key = self.get_key(film_id, user_id)
        await self._producer.send_and_wait(
            topic="views",
            value=self.serialize_int(number_seconds_viewing),
            key=kafka_key,
        )


viewing_timestamp_repository: ViewingKafkaRepository | None = None


def get_viewing_timestamp_repository() -> ViewingKafkaRepository:
    return viewing_timestamp_repository
