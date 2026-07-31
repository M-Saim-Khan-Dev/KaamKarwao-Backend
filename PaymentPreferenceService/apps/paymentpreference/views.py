from django.shortcuts import render
from .models import PaymentPreference
from .serializers import PraymentPreferenceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django.utils import timezone
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List PaymentPreference", description="Returns NonDeleted PaymentPreference for the Authenticated users"),
    create=extend_schema(summary="Create PaymentPreference by Admin Users"),
    retrieve= extend_schema(summary="Get a particular PaymentPreference"),
    update=extend_schema(summary="Fully Update PaymentPreference"),
    partial_update=extend_schema(summary="Partially Update PaymentPreference"),
    destroy=extend_schema(summary="Soft-delete PaymentPreference, setting deleted time to now"),
)

class CreatePaymentPreferenceView(viewsets.ModelViewSet):
    queryset = PaymentPreference.objects.filter(deleted_at__isnull=True)
    serializer_class = PraymentPreferenceSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
     
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
    
