import json
import asyncio
from decimal import Decimal, InvalidOperation
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Bid
from .serializers import BidSerializer
from .internal_client import set_task_worker

HEARTBEAT_INTERVAL_SECONDS = 10

class BiddingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope["url_route"]["kwargs"]['task_id']
        self.group_name= f"bidding_{self.task_id}"

        already_closed = await self.is_bidding_closed()
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

        if already_closed:
            await self.send(text_data=json.dumps({
                "type": "bidding_closed",
                "message": "Bidding for this task has already ended.",
            }))
            await self.close()
            return
        
        bids = await self.get_existing_bids()
        await self.send(text_data=json.dumps({
            "type": "bid_history",
            "bids": bids,
        }))

        self.heartbeat_task = asyncio.ensure_future(self.heartbeat_loop())
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self,'heartbeat_task'):
            self.heartbeat_task.cancel()
    
    async def heartbeat_loop(self):
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)
                await self.send(text_data=json.dumps({
                    "type": "heartbeat",
                    "task_id": self.task_id,
                }))
        except asyncio.CancelledError:
            pass
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return
        
        action = data.get("type")

        if action == "place_bid":
            await self.handle_place_bid(data)
        elif action == "accept_bid":
            await self.handle_accept_bid(data)
        else:
            await self.send(text_data=json.dumps({"error": f"Unknown action : {action}"}))

    async def handle_place_bid(self,data):
        user_id = data.get("user_id")
        price = data.get("price")
        estimated_hours = data.get("estimated_hours")

        if not user_id or price is None:
            await self.send(text_data=json.dumps({"error": "user_id and price are required"}))
            return
        
        try:
            price = Decimal(str(price))
        except InvalidOperation:
            await self.send(text_data=json.dumps({"error": "Price must be a valid number"}))
            return
        
        bid = await self.create_bid(user_id,price,estimated_hours)

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "bid_placed", "bid": BidSerializer(bid).data},
        )

    async def handle_accept_bid(self,data):
        bid_id = data.get("bid_id")
        if not bid_id:
            await self.send(text_data=json.dumps({"error": "bid_id is required"}))
            return
        
        bid = await self.accept_bid(bid_id)
        if bid is None:
            await self.send(text_data=json.dumps({"error": "Bid is not found for this task"}))
            return
        
        success = await database_sync_to_async(set_task_worker)(self.task_id, bid.user_id)
        if not success:
            await self.send(text_data=json.dumps({
                "error": "Bid accepted, but failed to update task worker. Please retry or contact support."
            }))

        await self.channel_layer.group_send(
            self.group_name,
            {"type": "bid_accepted", "bid": BidSerializer(bid).data},
        )

    @database_sync_to_async
    def is_bidding_closed(self):
        return Bid.objects.filter(task_id = self.task_id, is_accepted = True).exists()
    
    @database_sync_to_async
    def get_existing_bids(self):
        bids = Bid.objects.filter(task_id = self.task_id, deleted_at__isnull=True)
        return BidSerializer(bids, many=True).data
    
    @database_sync_to_async
    def create_bid(self, user_id, price, estimated_hours):
        return Bid.objects.create(
            task_id = self.task_id,
            user_id = user_id,
            price = price,
            estimated_hours = estimated_hours,
            created_by = user_id,
        )
    
    @database_sync_to_async
    def accept_bid(self, bid_id):
        try:
            bid = Bid.objects.get(id = bid_id, task_id = self.task_id)
        except Bid.DoesNotExist:
            return None
        bid.is_accepted = True
        bid.save()
        return bid
    
    async def bid_placed(self,event):
        await self.send(text_data= json.dumps({
            "type": "bid_placed",
            "bid": event["bid"],
        }))

    async def bid_accepted(self, event):
        await self.send(text_data=json.dumps({
            "type": "bid_accepted",
            "bid": event["bid"],
        }))
        if hasattr(self, 'heartbeat_task'):
            self.heartbeat_task.cancel()
        await self.close()