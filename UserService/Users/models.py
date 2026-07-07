from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length = 15)
    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True)
    username = None
    email= models.EmailField(unique= True)
    location_id = models.IntegerField(null=True, blank=True)
    location_zip_code = models.PositiveSmallIntegerField(null=True, blank=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name="creations")
    deleted_by= models.ForeignKey('self', null= True, blank = True, related_name="deletions", on_delete=models.SET_NULL)
    gender = models.CharField(max_length=12)
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.ForeignKey('UserType', on_delete=models.SET_NULL, null=True, related_name='users')
    image = models.CharField(max_length=200, null=True, blank=True)
