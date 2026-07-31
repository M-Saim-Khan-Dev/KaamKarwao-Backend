import json
import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

HEARTBEAT_INTERVAL_SECONDS = 10     #change according to time needed for heartbeat 
logger = logging.getLogger(__name__)

class TaskConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "tasks_feed"

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

        self.heartbeat_task = asyncio.ensure_future(self.heartbeat_loop())
        logger.info("Task feed websocket connected channel=%s", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
        if hasattr(self, 'heartbeat_task'):
            self.heartbeat_task.cancel()
        logger.info("Task feed websocket disconnected channel=%s close_code=%s", self.channel_name, close_code)

    async def heartbeat_loop(self):
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
                await self.send(text_data=json.dumps({
                    "type": "heartbeat",
                    "task":None,
                }))
        except asyncio.CancelledError:
            pass

    async def task_created(self,event):
        logger.info("Broadcasting task created task_id=%s", event["task"].get("id"))
        await self.send(text_data=json.dumps({
            "type": "task_created",
            "task": event["task"],
        }))

    async def task_deleted(self,event):
        logger.info("Broadcasting task deleted task_id=%s", event["task_id"])
        await self.send(text_data=json.dumps({
            "type": "task_deleted",
            "task_id": event["task_id"],
            "worker_id": event["worker_id"],
        }))

    async def task_assigned(self, event):
        logger.info("Broadcasting task assigned task_id=%s worker_id=%s", event["task_id"], event["worker_id"])
        await self.send(text_data=json.dumps({
            "type": "task_assigned",
            "task_id": event["task_id"],
            "worker_id": event["worker_id"],
        }))
