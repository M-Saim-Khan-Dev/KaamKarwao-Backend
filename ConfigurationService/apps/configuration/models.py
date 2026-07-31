from django.db import models

# Create your models here.
class Configuration(models.Model):
    attachments = models.PositiveSmallIntegerField()
    row_items = models.PositiveSmallIntegerField()