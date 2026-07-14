from django.core.management.base import BaseCommand
from Category.models import Category

class Command(BaseCommand):
    help = "Seeds initial Category data"

    def handle(self,*args,**options):
        Category_names = [
            "Tutor",
            "Plumber",
            "Electrician",
            "Cleaner",
            "Cook",
            "Driver",
        ]
        
        for name in Category_names:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Category: {name}"))
            
            else:
                self.stdout.write(f"Already exists: {name}")
        
        self.stdout.write(self.style.SUCCESS("Category seeding complete."))