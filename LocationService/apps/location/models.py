from django.db import models

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=15)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null = True, related_name = 'areas')
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
    formatted_address = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=10 , decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10 , decimal_places=7,null=True, blank=True)
    zip_code = models.IntegerField()
    deleted_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by_id=models.IntegerField(null=True, blank=True)
    deleted_by_id= models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.house_number} {self.street_number}, {self.formatted_address}"
