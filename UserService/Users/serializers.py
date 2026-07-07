from .models import User, UserType
from rest_framework import serializers

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
        user_type = UserTypeSerializer(read_only = True)
        usertype_id = serializers.PrimaryKeyRelatedField(
        queryset=UserType.objects.all(),source='user_type',write_only=True
    )
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
            "usertype_id",
            "location_id",
            "location_zip_code",
            "created_at",
            ]
            extra_kwargs = {"password" : {"write_only" : True}}

        def create(self, validated_data):
            password = validated_data.pop("password")

            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user

class UpdateImageSerializer(serializers.ModelSerializer):
     class Meta:
          model=User
          fields = ["Image"]