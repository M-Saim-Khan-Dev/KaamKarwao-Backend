from django.db import models

# Create your models here.

class Attachment(models.Model):
    url = models.URLField(blank=True, null=True)
    task_id = models.IntegerField(null=True, blank=True)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)