from rest_framework import serializers
from .models import WorkerEarnings

class WorkerEarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerEarnings
        fields = ["worker_id", "daily_earning", "weekly_earning", "total_earning", "total_jobs_done", "updated_at","daily_jobs_done"]