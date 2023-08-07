from datetime import datetime
from uuid import UUID
from typing import Generator

from pydantic import BaseModel
from kafka.consumer.fetcher import ConsumerRecord

from core.backoff import backoff


class DataValidator(BaseModel):
    user_id: UUID
    film_id: UUID
    number_seconds_viewing: int
    record_time: datetime


class DataTransformer:
    def transform(self, data: Generator[ConsumerRecord, None, None]):
        return self._transform_json(data)

    @backoff()
    def _transform_json(self, messages) -> Generator[DataValidator, None, None]:
        for record in messages:
            user_id, film_id = record.key.decode("utf-8").split(":")
            number_seconds_viewing = int.from_bytes(record.value, "big")
            record_time = datetime.fromtimestamp(record.timestamp / 1000)

            yield DataValidator(
                user_id=UUID(user_id),
                film_id=UUID(film_id),
                number_seconds_viewing=number_seconds_viewing,
                record_time=record_time,
            )


def get_transformer():
    return DataTransformer()
