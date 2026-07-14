from .models import Area, Country, City, Location
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
            "id",
            "house_number",
            "street_number",
            "formatted_address",
            "latitude",
            "longitude",
            "zip_code",
            "area",
            "city",
            "country", 
            "area_id",
            "city_id",
            "country_id",
            "created_at"
        ]

