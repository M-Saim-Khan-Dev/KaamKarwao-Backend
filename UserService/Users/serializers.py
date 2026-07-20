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
            "image"
            ]
            extra_kwargs = {"password" : {"write_only" : True}}

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user
        
        def update(self, instance, validated_data):
             password = validated_data.pop("password", None)
             for attr, value in validated_data.items():
                  setattr(instance, attr, value)
             if password:
                  instance.set_password(password)
             instance.save()
             return instance

class UpdateImageSerializer(serializers.ModelSerializer):
     file = serializers.ImageField(write_only=True, required=True)
     class Meta:
          model=User
          fields = ["image", "file"]
          read_only_fields = ["image"]

     def validate_file(self, value):
        max_size_mb = 5
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"File must be under {max_size_mb}MB")

        allowed_types = ["image/jpg", "image/png", "image/webp", "image/jpeg"]
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, or WEBP files are allowed")

        return value

class UpdateUserIsVerifiedSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ["is_verified"]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "location_id",
            "gender",
            "overall_rating",
            "is_verified",
            "usertype_id",
            "image",
        ]