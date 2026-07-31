from celery import shared_task
from .models import WorkerEarnings

@shared_task
def reset_daily_earnings():
    updated = WorkerEarnings.objects.update(daily_earning = 0, daily_jobs_done = 0)
    return f"Reset daily earnings for {updated} workers"

@shared_task
def reset_weekly_earnings():
    updated = WorkerEarnings.objects.update(weekly_earning=0)
    return f"Reset weekly earnings for {updated} workers"