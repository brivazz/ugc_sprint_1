import logging
from uuid import UUID
import datetime


from db.redis.base import RedisStorage


class ViewingCacheRepository(RedisStorage):
    @staticmethod
    def get_key(film_id: UUID, user_id: UUID) -> str:
        return str(user_id) + ":" + str(film_id)

    async def get_number_seconds_viewing(self, user_id: UUID, film_id: UUID):
        key = self.get_key(film_id, user_id)
        return await self._get(key)

    async def add_number_seconds_viewing(
        self, user_id: UUID, film_id: UUID, number_seconds_viewing: int
    ):
        key = self.get_key(film_id, user_id)
        await self._set(key, number_seconds_viewing)


viewing_cache_repository: ViewingCacheRepository | None = None


def get_viewing_cache_repository() -> ViewingCacheRepository:
    return viewing_cache_repository
