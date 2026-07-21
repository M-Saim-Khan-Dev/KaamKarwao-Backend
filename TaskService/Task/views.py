from .serializers import TaskSerializer
from .models import Task
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Task", description="Returns NonDeleted Task for the Authenticated users"),
    create=extend_schema(summary="Create Task"),
    retrieve= extend_schema(summary="Get a particular Task"),
    update=extend_schema(summary="Fully Update Task"),
    partial_update=extend_schema(summary="Partially Update Task"),
    destroy=extend_schema(summary="Soft-delete Task, setting deleted time to now"),
)

class CreateTaskView(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted_at__isnull=True)
    serializer_class = TaskSerializer
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()


@extend_schema(
        summary="Get a NonDeleted Task using the id of the user who created it",
)
class GetTaskByCreatedByView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        created_by = self.kwargs['created_by']
        return Task.objects.filter(created_by = created_by, deleted_at__isnull = True)