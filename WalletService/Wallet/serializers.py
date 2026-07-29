from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "user_id","amount","created_at"]
        read_only_fields = ['sender_id', 'sequence']