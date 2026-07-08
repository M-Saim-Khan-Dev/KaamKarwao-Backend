from .models import  UserType
from rest_framework import serializers

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']