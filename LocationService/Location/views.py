from django.shortcuts import render
from rest_framework import viewsets
from django.utils import timezone
from .serializers import AreaSerializer, CountrySerializer, CitySerializer,LocationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Area, City, Country, Location
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.
GOOGLE_FIELDS = {"latitude", "longitude", "formatted_address" }
USER_FIELDS = {"house_number", "street_number","area_id", "city_id", "country_id", "zip_code" }
ALLOWED_FIELDS = GOOGLE_FIELDS | USER_FIELDS

@extend_schema_view(
    list = extend_schema(summary="List Locations", description="Returns NonDeleted Locations"),
    create=extend_schema(summary="Create Locations"),
    retrieve= extend_schema(summary="Get one specific Location"),
    update=extend_schema(summary="Fully Update Locations"),
    partial_update=extend_schema(summary="Partially Update Locations"),
    destroy=extend_schema(summary="Soft-delete Locations, setting deleted time to now"),
)

class CreateLocationView(viewsets.ModelViewSet):
    queryset = Location.objects.filter(deleted_at__isnull=True)
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
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

@extend_schema_view(
    list = extend_schema(summary="List Areas", description="Returns NonDeleted Areas for the users"),
    create=extend_schema(summary="Create Areas by Admin Users"),
    retrieve= extend_schema(summary="Get one specific Area"),
    update=extend_schema(summary="Fully Update Areas"),
    partial_update=extend_schema(summary="Partially Update Areas"),
    destroy=extend_schema(summary="Delete Areas"),
)

class CreateAreaView(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    

@extend_schema_view(
    list = extend_schema(summary="List Cities", description="Returns NonDeleted Cities for the users"),
    create=extend_schema(summary="Create Cities by Admin Users"),
    retrieve= extend_schema(summary="Get one specific City"),
    update=extend_schema(summary="Fully Update Cities"),
    partial_update=extend_schema(summary="Partially Update Cities"),
    destroy=extend_schema(summary="Delete Cities"),
)

class CreateCityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

@extend_schema_view(
    list = extend_schema(summary="List Countries", description="Returns NonDeleted Countries for the users"),
    create=extend_schema(summary="Create Countries by Admin Users"),
    retrieve= extend_schema(summary="Get one specific Country"),
    update=extend_schema(summary="Fully Update Countries"),
    partial_update=extend_schema(summary="Partially Update Countries"),
    destroy=extend_schema(summary="Delete Countries"),
)


class CreateCountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]