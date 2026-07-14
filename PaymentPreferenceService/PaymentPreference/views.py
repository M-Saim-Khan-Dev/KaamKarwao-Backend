from django.shortcuts import render
from .models import PaymentPreference
from .serializers import PraymentPreferenceSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets

# Create your views here.

class CreatePaymentPreferenceView(viewsets.ModelViewSet):
    queryset = PaymentPreference.objects.all()
    serializer_class = PraymentPreferenceSerializer
    def get_permissions(self):
        return [IsAuthenticated()]
