from rest_framework import serializers
from .models import Bid

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "task_id",
            "user_id",
            "price",
            "is_accepted",
            "estimated_hours",
            "created_by",
            "created_at",
        ]
        read_only_fields = ["id", "is_accepted", "created_at"]