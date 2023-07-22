import json
from kafka import KafkaConsumer
from config import KAFKA_SERVER,TOPIC
from database.sqlite import insert_data,create_table
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)


def setup():
    create_table(query=Path("sql/create_table_clickstream_data.sql").read_text())


def get_consumer(group_name="gp-11"):

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=json.loads,
        auto_offset_reset="latest",
        group_id=group_name
    )
    consumer.subscribe(TOPIC)
    return consumer


def save_data(consumer):
    for data in consumer:
        logging.info(f'{data.value}')
        insert_data(
            [tuple(data.value)],
            query=Path("sql/insert_into_clickstream_data.sql").read_text()
        )


def main():
    setup()
    save_data(get_consumer())


if __name__ == '__main__':
   main()