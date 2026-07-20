from django.db import models

# Create your models here.
class Task(models.Model):
    subject = models.CharField(max_length=300)
    body = models.TextField()
    price = models.PositiveIntegerField()
    created_by = models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_by_id= models.IntegerField(null=True, blank=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
    preferred_time = models.CharField()
    location_id = models.IntegerField()
    status_id = models.IntegerField()
    payment_preference_id = models.IntegerField()
    accurately_estimated = models.IntegerField()
    category_id = models.IntegerField()
    worker_id = models.IntegerField(null=True, blank=True)
