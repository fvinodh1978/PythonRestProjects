# myapp/management/commands/runapscheduler.py
from django.core.management.base import BaseCommand
import apscheduler.schedulers.background
from apscheduler.triggers.interval import IntervalTrigger
import django_apscheduler.jobstores
import django_apscheduler.models
import logging
import time

logger = logging.getLogger(__name__)

def my_job():
    logger.info("My job is running...")
    # Your job logic here
    print("Vinodh")

class Command(BaseCommand):
    help = 'Runs APScheduler.'

    def handle(self, *args, **options):
        scheduler = apscheduler.schedulers.background.BackgroundScheduler()
        scheduler.add_jobstore(django_apscheduler.jobstores.DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=IntervalTrigger(seconds=30),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")