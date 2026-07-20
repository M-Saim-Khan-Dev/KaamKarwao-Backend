from .models import Task
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'subject',
            'body',
            'price',
            'created_at',
            'created_by',
            'preferred_time',
            'location_id',
            'status_id',
            'payment_preference_id',
            'accurately_estimated',
            'category_id',
            'worker_id', #worker id
        ]