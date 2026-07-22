from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task
from .serializers import TaskSerializer

@receiver(post_save, sender= Task)
def broadcast_task_events(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    if created:
        async_to_sync(channel_layer.group_send)(
            "tasks_feed",
            {
                "type": "task_created",
                "task": TaskSerializer(instance).data,
            }
        )
        return
    
    if getattr(instance, '_just_deleted', False):
        async_to_sync(channel_layer.group_send)(
            "tasks_feed",
            {
                "type": "task_deleted",
                "task_id": instance.id,
                "worker_id": instance.worker_id,
                "deleted_by": instance.deleted_by_id,
            }
        )