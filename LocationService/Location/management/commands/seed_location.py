# Location/management/commands/seed_test_location.py
from django.core.management.base import BaseCommand
from Location.models import Location, Area, City, Country

class Command(BaseCommand):
    help = "Seeds a single test location"

    def handle(self, *args, **options):
        area = Area.objects.get(name="DHA Phase 5")
        city = City.objects.get(name="Lahore")
        country = Country.objects.get(name="Pakistan")

        location, created = Location.objects.get_or_create(
            id=5,
            defaults={
                "house_number": 12,
                "street_number": "45B",
                "zip_code": "54000",
                "latitude": 31.4697,
                "longitude": 74.2728,
                "formatted_address": "DHA Phase 5, Lahore",
                "area": area,
                "city": city,
                "country": country,
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created location id={location.id}"))
        else:
            self.stdout.write(f"Location id=5 already exists")