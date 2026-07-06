from django.contrib import admin
from .models import UserType, Country, City, Area
# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(UserType)