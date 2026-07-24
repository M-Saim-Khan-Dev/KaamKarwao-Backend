from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    color = models.CharField(max_length=10)
    image = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length= 200)
    color = models.CharField(max_length=10)
    image = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='subcategories')
    base_price = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name