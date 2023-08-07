import logging

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


load_dotenv()


class Settings(BaseSettings):
    project_name: str = Field("movies", env="ETL_PROJECT_NAME")

    kafka_topic: str = Field("views", env="KAFKA_TOPIC")
    kafka_servers_str: str = Field(..., env="KAFKA_SERVERS")
    kafka_auto_offset_reset: str = Field("earliest", env="KAFKA_AUTO_OFFSET_RESET")
    kafka_group_id: str = Field(..., env="KAFKA_GROUP_ID")

    clickhouse_host: str = Field(..., env="CLICKHOUSE_HOST")
    clickhouse_port: int = Field(9000, env="CLICKHOUSE_PORT")
    clickhouse_table: str = Field(..., env="CLICKHOUSE_TABLE")

    @property
    def kafka_servers(self):
        return self.kafka_servers_str.split(",")

    def create_kafka_config(self):
        return {
            "topic": self.kafka_topic,
            "bootstrap_servers": self.kafka_servers,
            "auto_offset_reset": self.kafka_auto_offset_reset,
            "group_id": self.kafka_group_id,
        }

    def create_clickhouse_config(self):
        return {
            "host": self.clickhouse_host,
            "port": self.clickhouse_port,
        }


settings = Settings()


logger_settings = {
    "format": "%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "level": logging.INFO,
    "handlers": [logging.StreamHandler()],
}
