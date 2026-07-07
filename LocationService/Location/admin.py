from django.contrib import admin
from .models import Country,City,Area,Location
# Register your models here.
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Location)