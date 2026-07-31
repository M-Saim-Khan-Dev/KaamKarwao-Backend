from django.shortcuts import render
from .serializers import ConfigurationSerializer
from .models import Configuration
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets

# Create your views here.

class ConfigurationView(viewsets.ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    permission_classes = [IsAdminUser]