from django.core.management.base import BaseCommand
from Location.models import Country

class Command(BaseCommand):
    help = "Seeds initial Country data"

    def handle(self, *args, **options):
        country_names = [
            "Pakistan",
        ]

        for name in country_names:
            country, created = Country.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Country: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

        self.stdout.write(self.style.SUCCESS("Country seeding complete."))