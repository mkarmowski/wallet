from wallet import celery_app
from celery import task
from celery.schedules import crontab


@task
def setup_recurring_transaction(sender, week=None, month=None,
                                week_day=None, month_day=None, **kwargs):

    if week:
        sender.add_periiodic_task(
            crontab(hour=12, minute=0, day_of_week=week_day)
        )

    if month:
        sender.add_periiodic_task(
            crontab(hour=12, minute=0, day_of_month=month_day)
        )
