from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AreaSerializer, CountrySerializer, CitySerializer,LocationSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Area, City, Country, Location
# Create your views here.

class CreateLocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]

class CreateAreaView(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]

class CreateCityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CreateCountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]