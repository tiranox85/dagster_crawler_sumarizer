"""Collection of schedules"""

from dagster import schedule

from dagster_project.jobs import full_pipeline


# https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules
@schedule(
    cron_schedule="*/15 * * * *",
    job=full_pipeline,
    execution_timezone="US/Eastern",
)
def every_15m(context):
    """
    Runs full_pipeline every 15 minutes with empty run config.
    """
    return {}  # No extra config needed
