from django.db import models

class WorkerEarnings(models.Model):
    worker_id = models.IntegerField(unique=True)
    daily_earning = models.PositiveIntegerField(default=0)
    weekly_earning = models.PositiveIntegerField(default=0)
    total_earning = models.PositiveIntegerField(default=0)
    total_jobs_done = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    daily_jobs_done = models.PositiveIntegerField(default=0)
