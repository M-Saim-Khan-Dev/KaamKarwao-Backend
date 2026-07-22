from .serializers import TaskSerializer
from .models import Task
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics
from drf_spectacular.utils import extend_schema,extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

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
    queryset = Task.objects.filter(deleted_at__isnull=True).exclude(status_id=5)
    serializer_class = TaskSerializer
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.deleted_by_id = self.request.user.id
        instance._just_deleted = True
        instance.save()


@extend_schema(
        summary="Get a NonDeleted Task using the id of the user who created it",
)
class GetTaskByCreatedByView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        created_by = self.kwargs['created_by']
        return Task.objects.filter(created_by = created_by, deleted_at__isnull = True).exclude(status_id=5)
    

@extend_schema(
    summary="Get all Tasks with no worker assigned yet",
    description="Returns NonDeleted Tasks where worker_id is not filled, i.e. open for bidding",
)
class GetOpenTasksView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(worker_id__isnull=True, deleted_at__isnull=True).exclude(status_id=5)
    

@extend_schema(
    summary="Get NonDeleted Tasks assigned to a particular worker",
)
class GetTaskByWorkerView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        worker_id = self.kwargs['worker_id']
        return Task.objects.filter(
            worker_id=worker_id,
            deleted_at__isnull=True,
        ).exclude(status_id=5)

@extend_schema(exclude=True)  
class InternalSetTaskWorkerView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, task_id):
        secret = request.headers.get('X-Internal-Secret')
        if secret != settings.INTERNAL_SERVICE_SECRET:
            raise PermissionDenied("Not authorized")

        worker_id = request.data.get("worker_id")
        if not worker_id:
            return Response({"error": "worker_id is required"}, status=400)

        try:
            task = Task.objects.get(id=task_id, deleted_at__isnull=True)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        task.worker_id = worker_id
        task.save()

        return Response({"task_id": task_id, "worker_id": worker_id})