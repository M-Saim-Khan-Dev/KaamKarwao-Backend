from django.shortcuts import render
from .models import Attachment
from .serializers import AttachmentSerializer
from .supabase_client import upload_to_supabase
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

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
