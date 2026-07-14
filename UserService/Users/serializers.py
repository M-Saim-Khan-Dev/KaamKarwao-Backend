from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields=[
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "overall_rating",
            "is_verified",
            "password",
            "usertype_id",
            "location_id",
            "location_zip_code",
            "created_at",
            ]
            extra_kwargs = {"password" : {"write_only" : True}}
        WORKER_TYPE_ID = 3
        WORKER_ONLY_FIELDS = ["daily_earning", "weekly_earning", "total_earning", "jobs_done"]

        def create(self, validated_data):
            password = validated_data.pop("password")

            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        
        def to_representation(self, instance):
           data = super().to_representation(instance)
           if instance.usertype_id == self.WORKER_TYPE_ID:
            for field in self.WORKER_ONLY_FIELDS:
               data[field] = getattr(instance, field)
           return data

class UpdateImageSerializer(serializers.ModelSerializer):
     class Meta:
          model=User
          fields = ["image"]

class UpdateUserIsVerifiedSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ["is_verified"]