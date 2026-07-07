from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Location
from .events import publish_location_updated

@receiver(post_save,sender=Location)
def location_saved(sender,instance, created, **kwargs):
    publish_location_updated(instance)