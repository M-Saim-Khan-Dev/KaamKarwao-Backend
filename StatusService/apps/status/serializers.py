from .models import Status
from rest_framework import serializers

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
            'id',
            'name',
            'created_at'
        ]