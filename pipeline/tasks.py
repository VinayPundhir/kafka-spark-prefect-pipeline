from prefect import task

from broker.consumers import save_click_data_into_db
from broker.producers import click_data
from transformations import aggregate_and_index


@task
def generate_clickstream():
    click_data.main()


@task
def save_clickstream_in_db():
    save_click_data_into_db.main()


@task()
def aggregate_and_push_in_index():
    aggregate_and_index.main()
