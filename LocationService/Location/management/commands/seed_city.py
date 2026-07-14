from django.core.management.base import BaseCommand
from Location.models import City

class Command(BaseCommand):
    help = "Seeds initial City data"

    def handle(self, *args, **options):
        city_names = [
            "Lahore",
            "Karachi",
            "Islamabad",
            "Rawalpindi",
            "Faisalabad",
        ]

        for name in city_names:
            city, created = City.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created City: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

        self.stdout.write(self.style.SUCCESS("City seeding complete."))