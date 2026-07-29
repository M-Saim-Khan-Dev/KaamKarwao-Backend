from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
import requests
from .models import Message
from .serializers import MessageSerializer
import time
from django.conf import settings
from agora_token_builder import RtcTokenBuilder

Role_Publisher = 1 

# Create your views here.

TASK_SERVICE_URL = "http://127.0.0.1:8007"


class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(summary="List Message's info"),
    create=extend_schema(summary="Create Message for Authenticated Users"),
    retrieve=extend_schema(summary="Get one user's Message"),
    update=extend_schema(summary="Fully Update Message"),
    partial_update=extend_schema(summary="Partially Update Message"),
    destroy=extend_schema(summary="Soft Delete Message"),
)
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get_permissions(self):
        if self.action == 'admin_room_messages':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = Message.objects.filter(deleted_at__isnull=True)

        room_id = self.request.query_params.get('room_id')
        if room_id:
            qs = qs.filter(room_id=room_id)

        before = self.request.query_params.get('before')
        if before:
            qs = qs.filter(sequence__lt=before)

        return qs.order_by('-sequence')

    def perform_create(self, serializer):
        requesting_user_id = int(self.request.headers.get('X-User-Id'))
        serializer.save(sender_id=requesting_user_id)

    def perform_update(self, serializer):
        message = self.get_object()
        requesting_user_id = int(self.request.headers.get('X-User-Id'))
        if message.sender_id != requesting_user_id:
            raise PermissionDenied("You can only edit your own messages.")
        serializer.save()

    def perform_destroy(self, instance):
        requesting_user_id = int(self.request.headers.get('X-User-Id'))
        if instance.sender_id != requesting_user_id:
            raise PermissionDenied("You can only delete your own messages.")
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=False, methods=['get'], url_path='room/(?P<task_id>[^/.]+)/status')
    def room_status(self, request, task_id=None):
        try:
            response = requests.get(f"{TASK_SERVICE_URL}/internal/task/{task_id}/chat-status/", timeout=3)
        except requests.RequestException:
            return Response({"error": "Could not reach TaskService"}, status=502)

        if not response.ok:
            return Response({"error": "Task not found"}, status=404)

        data = response.json()
        user_id = int(request.headers.get('X-User-Id'))
        is_participant = user_id in {data["created_by"], data["worker_id"]}

        return Response({
            "task_id": task_id,
            "is_open": data["is_open"] and is_participant,
        })

    @extend_schema(
        summary="Get all messages for a room/task (Admin only)",
        description=(
            "Returns the full message history for a given room_id, including "
            "soft-deleted messages. Intended for moderation, disputes, or "
            "support use — bypasses normal chat-open checks entirely."
        ),
    )
    @action(detail=False, methods=['get'], url_path='admin/room/(?P<room_id>[^/.]+)')
    def admin_room_messages(self, request, room_id=None):

        qs = Message.objects.filter(room_id=room_id).order_by('sequence')

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='room/(?P<task_id>[^/.]+)/call-token')
    def call_token(self, request, task_id=None):
        try:
            response = requests.get(f"{TASK_SERVICE_URL}/internal/task/{task_id}/chat-status/", timeout=3)
        except requests.RequestException:
            return Response({"error": "Could not reach TaskService"}, status=502)

        if not response.ok:
            return Response({"error": "Task not found"}, status=404)

        data = response.json()
        user_id = int(request.headers.get('X-User-Id'))
        is_participant = user_id in {data["created_by"], data["worker_id"]}

        if not (data["is_open"] and is_participant):
            return Response({"error": "Call is not available for this task"}, status=403)

        channel_name = f"task_{task_id}"
        expiration_seconds = 3600  # 1 hour, not 24 — a call token living a full day is an unnecessarily long-lived credential
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expiration_seconds

        token = RtcTokenBuilder.buildTokenWithUid(
            settings.AGORA_APP_ID,
            settings.AGORA_APP_CERTIFICATE,
            channel_name,
            user_id, 
            Role_Publisher,
            privilege_expired_ts,
        )

        return Response({"token": token, "channel_name": channel_name, "app_id": settings.AGORA_APP_ID})