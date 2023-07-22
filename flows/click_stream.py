from prefect import task, flow
from prefect.task_runners import ConcurrentTaskRunner
from broker.producers import click_data
from broker.consumers import save_click_data_into_db


@task
def generate_clickstream():
    click_data.main()


@task
def save_clickstream_in_db():
    save_click_data_into_db.main()


@flow(name="click_stream",task_runner=ConcurrentTaskRunner())
def run_steps():
    generate_clickstream.submit()
    save_clickstream_in_db.submit()


if __name__=="__main__":
   run_steps()
