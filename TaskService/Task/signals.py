import requests
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Task
from .serializers import TaskSerializer

EARNING_SERVICE_URL = "http://127.0.0.1:8010"

@receiver(pre_save,sender = Task)
def stash_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_status_id = Task.objects.get(pk=instance.pk).status_id
        except Task.DoesNotExist:
            instance._old_status_id = None
    else:
        instance._old_status_id = None

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
        return
    
    old_status = getattr(instance,'_old_status_id', None)
    if instance.status_id == 4 and old_status != 4:
        if not instance.worker_id:
            print(f"Task {instance.id} marked complete but has no worker_id — skipping earning sync")
            return

        try:
            requests.post(
                f"{EARNING_SERVICE_URL}/earnings/internal/add/",
                json={"worker_id": instance.worker_id, "price": instance.price},
                timeout=3,
            )
        except requests.RequestException as e:
            print(f"Failed to sync earning for task {instance.id}: {e}")