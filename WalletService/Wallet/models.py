from django.db import models

# Create your models here.

class Wallet(models.Model):
    user_id = models.IntegerField(unique=True)
    amount = models.DecimalField(default = 0, decimal_places=2, max_digits= 8)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null = True, blank= True)
    deleted_by = models.IntegerField(null=True, blank=True)