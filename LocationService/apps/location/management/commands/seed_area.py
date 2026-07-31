from django.core.management.base import BaseCommand
from Location.models import Area,City,Country

class Command(BaseCommand):
    help = "Seeds initial Area data"

    def handle(self,*args,**options):
        Area_names = [
            "DHA Phase 5",
            "DHA Phase 6",
            "Gulberg III",
            "Model Town",
            "Johar Town",
            "Cantt",
            "Bahria Town",
            "Wapda Town",
            "Askari 10",
            "Iqbal Town'",
            "Township", 
            "Garden Town",
            "Valencia Town",
            "Faisal Town",
            "F-7 Markaz",
            "F-8 Markaz",
            "F-10",
            "G-11",
            "G-9",
            "E-7 Sector",
            "E-11",
            "DHA Phase 2",
            "Bahria Town Islamabad",
            "Bani Gala",
        ]
        
        for name in Area_names:
            area, created = Area.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Area: {name}"))
            
            else:
                self.stdout.write(f"Already exists: {name}")
        
        self.stdout.write(self.style.SUCCESS("Area seeding complete."))