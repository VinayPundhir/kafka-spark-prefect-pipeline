import json
import logging
from pathlib import Path

from kafka import KafkaConsumer

from config import KAFKA_SERVER, TOPIC
from database import create_table, insert_data

logging.basicConfig(level=logging.INFO)


def setup():
    """initialize tasks before running consumer"""
    create_table(query=Path("sql/create_table_clickstream_data.sql").read_text())


def get_consumer(group_name: str = "gp-1") -> KafkaConsumer:

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=json.loads,
        auto_offset_reset="latest",
        group_id=group_name,
    )
    consumer.subscribe(TOPIC)
    return consumer


def save_data(consumer: KafkaConsumer):
    """function saves consumed data from message broker into db"""
    for data in consumer:
        logging.info(f"{data.value}")
        insert_data(
            [tuple(data.value)],
            query=Path("sql/insert_into_clickstream_data.sql").read_text(),
        )


def main():
    setup()
    save_data(get_consumer())


if __name__ == "__main__":
    main()
