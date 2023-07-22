import json
from time import sleep
from kafka import KafkaProducer
from config import KAFKA_SERVER,TOPIC
from faker import Faker
from random import choice
import logging

logging.basicConfig(level=logging.INFO)


fake = Faker()
fake_urls = [fake.url() for _ in range(100)]
fake_countries = [fake.country() for _ in range(30)]
fake_usr_ids = [fake.uuid4() for _ in range(100)]


def generate_fake_data():
    user_id = choice(fake_usr_ids)
    timestamp = fake.date_time_this_month().isoformat()
    url = choice(fake_urls)
    country = choice(fake_countries)
    city = fake.city()
    browser = fake.chrome()
    os = fake.linux_platform_token()
    device = fake.word()
    return user_id, timestamp, url, country, city, browser, os, device


def get_producer():
    return KafkaProducer(
       bootstrap_servers=KAFKA_SERVER,
       value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_data(data, producer):
    producer.send(TOPIC, data)
    producer.flush()


def push_click_data(producer):
    """for sake of this project we assume producer will run continuously"""
    while True:
        data = generate_fake_data()
        logging.info(f'{data}')
        producer.send(TOPIC, data)
        sleep(1)


def main():
    producer = get_producer()
    push_click_data(producer)
    producer.close()


if __name__ == "__main__":
    main()