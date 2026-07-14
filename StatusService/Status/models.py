from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.IntegerField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    deleted_by_id= models.IntegerField(null=True, blank=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
