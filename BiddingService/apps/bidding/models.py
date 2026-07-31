from django.db import models

# Create your models here.
class Bid(models.Model):
    task_id = models.IntegerField()
    user_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_accepted = models.BooleanField(default=False)
    estimated_hours=models.PositiveIntegerField(null=True, blank=True)
    deleted_by = models.IntegerField(blank=True,null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)