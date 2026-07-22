import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

HEARTBEAT_INTERVAL_SECONDS = 10     #change according to time needed for heartbeat 

class TaskConsumer(AsyncWebsocketConsumer):
    GROUP_NAME = "tasks_feed"

    async def connect(self):
        await self.channel_layer.group_add(self.GROUP_NAME, self.channel_name)
        await self.accept()

        self.heartbeat_task = asyncio.ensure_future(self.heartbeat_loop())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.GROUP_NAME, self.channel_name)
        if hasattr(self, 'heartbeat_task'):
            self.heartbeat_task.cancel()

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
        await self.send(text_data=json.dumps({
            "type": "task_created",
            "task": event["task"],
        }))

    async def task_deleted(self,event):
        await self.send(text_data=json.dumps({
            "type": "task_deleted",
            "task_id": event["task_id"],
            "worker_id": event["worker_id"],
        }))