from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AreaSerializer, CountrySerializer, CitySerializer,LocationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Area, City, Country, Location
# Create your views here.

GOOGLE_FIELDS = {"latitude", "longitude", "formatted_address" }
USER_FIELDS = {"house_number", "street_number","area_id", "city_id", "country_id", "zip_code" }
ALLOWED_FIELDS = GOOGLE_FIELDS | USER_FIELDS

class CreateLocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]
    
    def update(self, request, *args,**kwargs):
        instance = self.get_object()

        incoming_keys=set(request.data.keys())
        filtered_data={
            key: value for key, value in request.data.items()
            if key in ALLOWED_FIELDS
        }

        google_keys_sent = incoming_keys & GOOGLE_FIELDS
        user_keys_sent = incoming_keys & USER_FIELDS

        if google_keys_sent and google_keys_sent != GOOGLE_FIELDS:
            missing = GOOGLE_FIELDS - google_keys_sent
            raise ValidationError({
                "error": f"Updating location requires all Google Fields together. Missing: {sorted(missing)}"
            })
        if not google_keys_sent and not user_keys_sent:
            raise ValidationError({"error": "No updatable fields provided"})
        
        serializer = self.get_serializer(instance, data=filtered_data, partial = True)
        serializer.is_valid(raise_exception= True)
        serializer.save()

        return Response(serializer.data)

class CreateAreaView(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class CreateCityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

class CreateCountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]