import datetime
import logging
from functools import lru_cache
from uuid import UUID
from typing import Protocol

from fastapi import Depends

from db.kafka_db.viewing import get_viewing_timestamp_repository
from db.redis.viewing import get_viewing_cache_repository


class ViewingCacheRepositoryProtocol(Protocol):
    async def get_number_seconds_viewing(self, user_id: UUID, film_id: UUID) -> int:
        """Добавление временной метки просмотренного сегмента фильма"""

    async def add_number_seconds_viewing(
        self, user_id: UUID, film_id: UUID, number_seconds_viewing: int
    ):
        """Получение временную метку для продолжения просмотра фильма"""


class ViewingRepositoryProtocol(Protocol):
    async def add_number_seconds_viewing(
        self, user_id: UUID, film_id: UUID, number_seconds_viewing: int
    ):
        """Получение временную метку для продолжения просмотра фильма"""


class MovieViewService:
    def __init__(
        self,
        viewing_timestamp_repository: ViewingRepositoryProtocol,
        viewing_cache_repository: ViewingCacheRepositoryProtocol,
    ):
        self._viewing_timestamp_repository = viewing_timestamp_repository
        self._viewing_cache_repository = viewing_cache_repository

    async def add_number_seconds_viewing(
        self, user_id: UUID, film_id: UUID, number_seconds_viewing: int
    ) -> None:
        await self._viewing_timestamp_repository.add_number_seconds_viewing(
            user_id, film_id, number_seconds_viewing
        )
        await self._viewing_cache_repository.add_number_seconds_viewing(
            user_id, film_id, number_seconds_viewing
        )

    async def get_number_seconds_viewing(
        self,
        user_id: UUID,
        film_id: UUID,
    ) -> int:
        number_seconds_viewing = (
            await self._viewing_cache_repository.get_number_seconds_viewing(
                user_id, film_id
            )
        )
        return number_seconds_viewing


@lru_cache()
def get_movie_view_service(
    viewing_repository: ViewingRepositoryProtocol = Depends(
        get_viewing_timestamp_repository
    ),
    viewing_cache_repository: ViewingCacheRepositoryProtocol = Depends(
        get_viewing_cache_repository
    ),
) -> MovieViewService:
    return MovieViewService(viewing_repository, viewing_cache_repository)
