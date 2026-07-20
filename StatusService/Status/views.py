from .serializers import StatusSerializer
from .models import Status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Status", description="Returns NonDeleted Status for the Authenticated users"),
    create=extend_schema(summary="Create Status"),
    retrieve= extend_schema(summary="Get a particular Status"),
    update=extend_schema(summary="Fully Update Status"),
    partial_update=extend_schema(summary="Partially Update Status"),
    destroy=extend_schema(summary="Soft-delete Status, setting deleted time to now"),
)

class CreateStatusView(viewsets.ModelViewSet):
    queryset = Status.objects.filter(deleted_at__isnull=True)
    serializer_class = StatusSerializer
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
