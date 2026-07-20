from django.shortcuts import render
from django.utils import timezone
from .models import Attachment
from .serializers import AttachmentSerializer
from .supabase_client import upload_to_supabase
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets,status, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Attachments", description="Returns NonDeleted Attachments for the Authenticated users"),
    create=extend_schema(summary="Create Attachments for Authenticated Users containing valid TaskId's"),
    retrieve= extend_schema(summary="Get one user's Attachment"),
    update=extend_schema(summary="Fully Update Attachments"),
    partial_update=extend_schema(summary="Partially Update Attachments"),
    destroy=extend_schema(summary="Soft-delete Attachments, setting deleted time to now"),
)

class CreateAttachmentView(viewsets.ModelViewSet):
    queryset = Attachment.objects.filter(deleted_at__isnull=True)
    serializer_class = AttachmentSerializer
    parser_classes = [MultiPartParser, FormParser]
    def get_permissions(self):
        return [IsAuthenticated()] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_id = request.data.get("task_id")
        if not task_id:
            return Response({"error": "task_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data["file"]
        url = upload_to_supabase(file)

        attachment = Attachment.objects.create(
            url=url,
            created_by=request.data.get("created_by"),
            task_id = task_id,
        )

        return Response(AttachmentSerializer(attachment).data, status = status.HTTP_201_CREATED)
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

@extend_schema(
        summary="Gets Attachment using TaskId",
    )
class GetAttachmentByTaskView(generics.ListAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Attachment.objects.filter(task_id=task_id, deleted_at__isnull=True)