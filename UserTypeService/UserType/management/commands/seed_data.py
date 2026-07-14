from django.core.management.base import BaseCommand
from UserType.models import UserType

class Command(BaseCommand):
    help = "Seeds initial UserType data"

    def handle(self,*args,**options):
        UserType_names = [
            "Admin",
            "Customer",
            "Worker",
        ]
        
        for name in UserType_names:
            user_type, created = UserType.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created UserType: {name}"))
            
            else:
                self.stdout.write(f"Already exists: {name}")
        
        self.stdout.write(self.style.SUCCESS("UserType seeding complete."))