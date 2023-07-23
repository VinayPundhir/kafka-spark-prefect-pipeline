from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from pipeline import flows


def deploy(timezone="Asia/Kolkata"):
    """
    flows for consumer and producer
    """

    Deployment.build_from_flow(
        flow=flows.generate_click_stream, name="prod", schedule=None
    ).apply()

    Deployment.build_from_flow(
        flow=flows.save_click_stream_in_db, name="prod", schedule=None
    ).apply()

    """
    flows for periodic transformation
    """

    Deployment.build_from_flow(
        flow=flows.aggregate_and_index,
        name="prod",
        schedule=(CronSchedule(cron="* */6 * * *", timezone=timezone)),
    ).apply()


if __name__ == "__main__":
    deploy()
