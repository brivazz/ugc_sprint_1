import json

from redis.asyncio import Redis


CACHE_EXPIRE_IN_SECONDS = 60 * 60 * 24 * 5


class RedisStorage:
    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    async def _get(self, key):
        return await self.redis.get(key)

    async def _set(self, key, value):
        await self.redis.set(key, value, ex=CACHE_EXPIRE_IN_SECONDS)

    def _key_generate(*args, **kwargs) -> str:
        return f'{args}:{json.dumps({"kwargs": kwargs}, sort_keys=True)}'

    async def close(self):
        await self.redis.close()


redis_storage: RedisStorage | None = None


# Функция понадобится при внедрении зависимостей
async def get_redis_storage() -> RedisStorage:
    return redis_storage
