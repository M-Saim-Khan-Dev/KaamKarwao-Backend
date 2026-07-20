from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Review (models.Model):
    user_id = models.IntegerField()
    task_id = models.IntegerField()
    given_by = models.IntegerField()
    body = models.TextField()
    attachment_id = models.IntegerField(null= True, blank=True)
    deleted_by = models.IntegerField(null=True, blank= True)
    deleted_at = models.DateTimeField(null= True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
