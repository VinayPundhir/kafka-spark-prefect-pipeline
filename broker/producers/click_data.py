import json
import logging
from random import choice
from time import sleep

from faker import Faker
from kafka import KafkaProducer

from config import KAFKA_SERVER, TOPIC

logging.basicConfig(level=logging.INFO)


fake = Faker()
fake_urls = [fake.url() for _ in range(100)]
fake_countries = [fake.country() for _ in range(30)]
fake_usr_ids = [fake.uuid4() for _ in range(100)]


def generate_fake_data() -> tuple:
    """
    function generates fake data for following fields :
        return user_id ,timestamp , url ,country ,city ,browser, os ,device
    """
    user_id = choice(fake_usr_ids)
    timestamp = fake.date_time_this_month().isoformat()
    url = choice(fake_urls)
    country = choice(fake_countries)
    city = fake.city()
    browser = fake.chrome()
    os = fake.linux_platform_token()
    device = fake.word()
    return user_id, timestamp, url, country, city, browser, os, device


def get_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_data(data: dict, producer: KafkaProducer):
    """sends data into message broker"""
    producer.send(TOPIC, data)
    producer.flush()


def produce_fake_data(producer: KafkaProducer, delay: int = 0.1):
    """function continuously creates fake click stream"""
    while True:
        data = generate_fake_data()
        logging.info(f"{data}")
        producer.send(TOPIC, data)
        sleep(delay)


def main():
    producer = get_producer()
    produce_fake_data(producer)
    producer.close()


if __name__ == "__main__":
    main()
