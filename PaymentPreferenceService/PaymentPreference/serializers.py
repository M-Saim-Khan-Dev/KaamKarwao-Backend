from .models import PaymentPreference
from rest_framework import serializers

class PraymentPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPreference
        fields=[
            "id",
            "name",
            "created_at"
        ]