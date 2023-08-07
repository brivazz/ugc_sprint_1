from typing import Any

from clickhouse_driver import Client

from core.backoff import backoff
from .data_transformer import DataValidator


class ClickHouseLoader:
    def __init__(self, client: Client) -> None:
        self.client = client

    @backoff()
    def create_database_and_table(self, table_name: str) -> None:
        self.client.execute(
            "CREATE DATABASE IF NOT EXISTS shard ON CLUSTER company_cluster"
        )
        self.client.execute(
            f"CREATE TABLE IF NOT EXISTS shard.{table_name} ON CLUSTER company_cluster \
                (user_id UUID, film_id UUID, number_seconds_viewing INTEGER, record_time DateTime) \
                    ENGINE = MergeTree() ORDER BY (user_id, film_id)"
        )

    @backoff()
    def load(self, table_name: str, data: list[DataValidator]) -> int | None:
        """Метод для загрузки данных в Clickhouse."""
        query = f"""
            INSERT INTO shard.{table_name}
            (user_id, film_id, number_seconds_viewing, record_time) VALUES"""

        return self.client.execute(
            query,
            (
                (
                    row.user_id,
                    row.film_id,
                    row.number_seconds_viewing,
                    row.record_time,
                )
                for row in data
            ),
        )


@backoff()
def get_clickhouse_loader(settings: dict[str, Any]):
    client = Client(
        host=settings["host"],
        port=settings["port"],
    )
    return ClickHouseLoader(client)
