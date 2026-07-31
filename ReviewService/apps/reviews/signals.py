import requests
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review

USER_SERVICE_URL = "http://127.0.0.1:8001"

def sync_user_rating(user_id):
    average_rating = Review.objects.filter(
        user_id=user_id, deleted_at__isnull=True
    ).aggregate(avg=Avg('rating'))['avg']

    rating_to_save = round(average_rating) if average_rating is not None else 5

    try:
        requests.patch(
            f"{USER_SERVICE_URL}/app/user/{user_id}/rating/internal/",
            json={"overall_rating" : rating_to_save},
            timeout=3,
        )
    except requests.RequestException as e:
        print (f"Failed to sync rating to user {user_id}: {e}")


@receiver(post_save, sender=Review)
def on_review_saved(sender,instance,**kwargs):
    sync_user_rating(instance.user_id)

@receiver(post_delete,sender = Review)
def on_review_deleted(sender, instance,**kwargs):
    sync_user_rating(instance.user_id)