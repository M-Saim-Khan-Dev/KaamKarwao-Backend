from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task
from .serializers import TaskSerializer

@receiver(post_save, sender= Task)
def broadcast_task_created(sender, instance, created, **kwargs):
    if not created:
        return 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "tasks_feed",
        {
            "type": "task_created",
            "task": TaskSerializer(instance).data,
        }
    )