from redis.asyncio import Redis
from db.redis import viewing


redis: Redis | None = None


def on_startup(host: str, port: int):
    global redis
    redis = Redis(host=host, port=port)
    viewing.viewing_cache_repository = viewing.ViewingCacheRepository(redis)


async def on_shutdown():
    await redis.close()
