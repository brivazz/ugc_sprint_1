from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import movie_views
from core.config import settings
from db.kafka_db import kafka_storage
from db.redis import redis_storage


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/v1/ugc/openapi",
    openapi_url="/api/v1/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    await kafka_storage.on_startup(settings.kafka_host, settings.kafka_port)
    redis_storage.on_startup(host=settings.redis_host, port=settings.redis_port)


@app.on_event("shutdown")
async def shutdown():
    redis_storage.on_shutdown()
    await kafka_storage.on_shutdown()


app.include_router(
    movie_views.router, prefix="/api/v1/ugc/movie_views", tags=["movie_view"]
)
