from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserType(models.Model):
    name = models.CharField(max_length = 15)
    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(null=True, unique=True)
    objects = CustomUserManager()
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email= models.EmailField(unique= True)
    location_id = models.IntegerField(null=True, blank=True)
    location_zip_code = models.PositiveSmallIntegerField(null=True, blank=True)
    deleted_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name="creations")
    deleted_by= models.ForeignKey('self', null= True, blank = True, related_name="deletions", on_delete=models.SET_NULL)
    gender = models.CharField(max_length=16, default="Not Specified")
    overall_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.ForeignKey('UserType', on_delete=models.SET_NULL, null=True, related_name='users')
    image = models.CharField(max_length=200, null=True, blank=True)
