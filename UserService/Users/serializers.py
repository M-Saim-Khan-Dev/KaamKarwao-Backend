from .models import User, UserType, Area, Country, City, Location
from rest_framework import serializers

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(),source='area',write_only=True
    )
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),source='country',write_only=True
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),source='city',write_only=True
    )
    area = AreaSerializer(read_only=True)
    city = CitySerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    class Meta:
        model = Location
        fields = [
            "house_number",
            "street_number",
            "landmark",
            "pin_location",
            "zip_code",
            "area",
            "city",
            "country", 
            "area_id",
            "city_id",
            "country_id" 
        ]

class UserSerializer(serializers.ModelSerializer):
        location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),source='location',write_only=True
    )
        location = LocationSerializer(read_only = True)
        user_type = UserTypeSerializer(read_only = True)
        usertype_id = serializers.PrimaryKeyRelatedField(
        queryset=UserType.objects.all(),source='user_type',write_only=True
    )
        class Meta:
            model = User
            fields=[
                "password",
                "first_name",
                "last_name",
                "phone_number",
                "email",
                "gender",
                "overall_rating",
                "user_type",
                "usertype_id",
                "location",
                "location_id",
            ]
            extra_kwargs = {"password" : {"write_only" : True}}