import json
import logging
import jwt as pyjwt
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Max
from .models import Message
from .serializers import MessageSerializer

TASK_SERVICE_URL = "http://127.0.0.1:8007"
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f"chat_{self.room_id}"
        logger.info("Chat websocket connection requested room_id=%s", self.room_id)

        query_string = self.scope['query_string'].decode()
        params = dict(qc.split('=') for qc in query_string.split('&') if '=' in qc)
        token = params.get('token')

        if not token:
            logger.warning("Chat websocket rejected: token missing room_id=%s", self.room_id)
            await self.close(code=4001)
            return

        try:
            payload = pyjwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        except pyjwt.InvalidTokenError:
            logger.warning("Chat websocket rejected: invalid token room_id=%s", self.room_id)
            await self.close(code=4001)
            return

        self.user_id = int(payload.get("user_id"))

        task_info = await self.get_task_chat_status(self.room_id)
        if task_info is None:
            logger.error("Chat websocket rejected: TaskService unavailable room_id=%s user_id=%s", self.room_id, self.user_id)
            await self.close(code=4004)
            return

        if not task_info["is_open"]:
            logger.warning("Chat websocket rejected: task closed room_id=%s user_id=%s", self.room_id, self.user_id)
            await self.close(code=4003)
            return

        allowed_users = {task_info["created_by"], task_info["worker_id"]}
        if self.user_id not in allowed_users:
            logger.warning("Chat websocket rejected: user not participant room_id=%s user_id=%s", self.room_id, self.user_id)
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info("Chat websocket connected room_id=%s user_id=%s", self.room_id, self.user_id)

        history = await self.get_message_history()
        await self.send(text_data=json.dumps({
            "type": "message_history",
            "messages": history,
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        logger.info("Chat websocket disconnected room_id=%s close_code=%s", getattr(self, "room_id", None), close_code)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logger.warning("Invalid chat websocket JSON room_id=%s user_id=%s", self.room_id, self.user_id)
            await self.send(text_data=json.dumps({"type": "error", "detail": "Invalid JSON"}))
            return
        if data.get("type") == "send_message":
            await self.handle_send_message(data)

    HISTORY_PAGE_SIZE = 50

    @database_sync_to_async
    def get_message_history(self):
        qs = Message.objects.filter(
            room_id=self.room_id, deleted_at__isnull=True
        ).order_by('-sequence')[:self.HISTORY_PAGE_SIZE]
        messages = list(reversed(qs))
        return MessageSerializer(messages, many=True).data

    @database_sync_to_async
    def create_message(self, body, reply_to_id, attachment_id):
        if reply_to_id is not None:
            exists = Message.objects.filter(
                id=reply_to_id, room_id=self.room_id, deleted_at__isnull=True
            ).exists()
            if not exists:
                raise ValueError(f"reply_to message {reply_to_id} does not exist in this room")

        last_sequence = Message.objects.filter(room_id=self.room_id).aggregate(
            max_seq=Max('sequence')
        )['max_seq'] or 0

        message = Message.objects.create(
            room_id=self.room_id,
            sender_id=self.user_id,
            body=body,
            attachment_id=attachment_id,
            reply_to_id=reply_to_id,
            sequence=last_sequence + 1,
        )
        return MessageSerializer(message).data

    @database_sync_to_async
    def _get_task_chat_status_sync(self, task_id):
        try:
            response = requests.get(f"{TASK_SERVICE_URL}/internal/task/{task_id}/chat-status/", timeout=3)
            if response.ok:
                return response.json()
        except requests.RequestException:
            pass
        return None

    async def get_task_chat_status(self, task_id):
        return await self._get_task_chat_status_sync(task_id)

    async def handle_send_message(self, data):
        body = data.get("body", "")
        reply_to_id = data.get("reply_to")
        attachment_id = data.get("attachment_id")

        if not body and not attachment_id:
            logger.warning("Rejected empty message room_id=%s user_id=%s", self.room_id, self.user_id)
            await self.send(text_data=json.dumps({"type": "error", "detail": "Message must have body or attachment_id"}))
            return

        try:
            message_data = await self.create_message(body, reply_to_id, attachment_id)
        except (ValueError, ObjectDoesNotExist, IntegrityError) as e:
            logger.warning("Rejected chat message room_id=%s user_id=%s reason=%s", self.room_id, self.user_id, e)
            await self.send(text_data=json.dumps({"type": "error", "detail": str(e)}))
            return

        await self.channel_layer.group_send(self.group_name, {
            "type": "message_received",
            "message": message_data,
        })
        logger.info("Chat message created room_id=%s user_id=%s message_id=%s", self.room_id, self.user_id, message_data["id"])

    async def message_received(self, event):
        await self.send(text_data=json.dumps({
            "type": "message_received",
            "message": event["message"],
        }))
