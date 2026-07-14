from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    color = models.TextField(max_length=9, null=True,blank=True)
    image = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name