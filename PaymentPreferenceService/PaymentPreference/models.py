from django.db import models

# Create your models here.
class PaymentPreference(models.Model):
    name = models.CharField(max_length=200)
    deleted_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)