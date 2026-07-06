from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length = 15)
    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=15)
    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length= 15)
    def __str__(self):
        return self.name


class Location(models.Model):
    house_number = models.SmallIntegerField()
    street_number = models.CharField(max_length=5)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null = True, related_name = 'locations')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null = True, related_name = 'locations')
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null = True, related_name = 'locations')
    landmark = models.CharField(max_length=30)
    pin_location = models.CharField(max_length=100)
    zip_code = models.PositiveSmallIntegerField()
    deleted_at=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="location_creations")
    deleted_by= models.ForeignKey('User', null= True, blank = True, related_name="location_deletions", on_delete=models.SET_NULL)


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True)
    email= models.EmailField(unique= True)
    location = models.ForeignKey('Location', on_delete=models.PROTECT, related_name = "users", null=True, blank=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name="creations")
    deleted_by= models.ForeignKey('self', null= True, blank = True, related_name="deletions", on_delete=models.SET_NULL)
    gender = models.CharField(max_length=12)
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.ForeignKey('UserType', on_delete=models.SET_NULL, null=True, related_name='users')
