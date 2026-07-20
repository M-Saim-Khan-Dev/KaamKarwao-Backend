from .models import Review
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'user_id',
            'task_id',
            'given_by',
            'body',
            'attachment_id',
            'created_at',
            'rating',
        ]