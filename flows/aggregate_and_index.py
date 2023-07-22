from prefect import task, flow
from transformations import aggregate_and_index


@task()
def aggregate_and_push_in_index():
    aggregate_and_index.main()


@flow(name="aggregate_and_index")
def run_steps():
    aggregate_and_push_in_index()


if __name__=="__main__":
    run_steps()
