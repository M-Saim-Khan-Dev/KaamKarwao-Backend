from celery import shared_task
import logging
from .models import WorkerEarnings

logger = logging.getLogger(__name__)

@shared_task
def reset_daily_earnings():
    logger.info("Starting daily earnings reset")
    updated = WorkerEarnings.objects.update(daily_earning = 0, daily_jobs_done = 0)
    logger.info("Completed daily earnings reset workers=%s", updated)
    return f"Reset daily earnings for {updated} workers"

@shared_task
def reset_weekly_earnings():
    logger.info("Starting weekly earnings reset")
    updated = WorkerEarnings.objects.update(weekly_earning=0)
    logger.info("Completed weekly earnings reset workers=%s", updated)
    return f"Reset weekly earnings for {updated} workers"
