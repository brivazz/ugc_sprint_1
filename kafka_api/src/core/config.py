import logging
import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings
from core.logger import LOGGING
from dotenv import load_dotenv

load_dotenv()
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = Field("movies", env="FAST_API_PROJECT_NAME")
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    redis_host: str = Field("127.0.0.1", env="REDIS_HOST")
    redis_port: int = Field("6379", env="REDIS_PORT")

    kafka_host: str = Field("127.0.0.1", env="KAFKA_PORT")
    kafka_port: int = Field("9092", env="KAFKA_PORT")
    kafka_topic: str = Field("views", env="KAFKA_TOPIC")

    auth_server_url: str = Field("http://nginx/api/v1/auth", env="AUTH_URL")


settings = Settings()
