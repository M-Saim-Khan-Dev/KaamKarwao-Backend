from django.db import models

# Create your models here.
class Configuration(models.Model):
    attachments = models.SmallIntegerField()
    row_items = models.SmallIntegerField()