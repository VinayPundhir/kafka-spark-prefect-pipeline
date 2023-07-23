from prefect import flow

from pipeline import tasks


@flow(name="aggregate_and_index")
def aggregate_and_index():
    tasks.aggregate_and_push_in_index()


@flow(name="generate_click_stream")
def generate_click_stream():
    tasks.generate_clickstream()


@flow(name="save_click_stream_in_db")
def save_click_stream_in_db():
    tasks.save_clickstream_in_db()
