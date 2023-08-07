import logging
import time

from etl.kafka_extractor import get_kafka_extractor
from etl.clickhouse_loader import get_clickhouse_loader
from etl.data_transformer import get_transformer

from src.core.config import settings, logger_settings


kafka_extractor = get_kafka_extractor(settings.create_kafka_config())
transformer = get_transformer()
clickhouse_loader = get_clickhouse_loader(settings.create_clickhouse_config())
clickhouse_loader.create_database_and_table(settings.clickhouse_table)

logging.basicConfig(**logger_settings)
logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("Starting etl...")
    storage = []
    while True:
        try:
            data = kafka_extractor.extract()
            for transformed_data in transformer.transform(data):
                storage.append(transformed_data)
                if len(storage) >= 1000:
                    if res := clickhouse_loader.load(
                        data=storage, table_name=settings.clickhouse_table
                    ):
                        logger.info(f"Insert {res} rows to ClickHouse.")
                        storage = []
                        kafka_extractor._commit()
        except Exception as er:
            logger.error("Error: %s", er)

        logger.info("Sleep %s seconds...", 5)
        time.sleep(5)
        continue


if __name__ == "__main__":
    main()
