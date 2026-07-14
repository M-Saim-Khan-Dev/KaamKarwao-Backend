from django.core.management.base import BaseCommand
from PaymentPreference.models import PaymentPreference

class Command(BaseCommand):
    help = "Seeds initial Payment_Preference data"

    def handle(self,*args,**options):
        Payment_Preference_names = [
            "Cash",
            "Card",
            "EasyPaisa",
        ]
        
        for name in Payment_Preference_names:
            payment_preference, created = PaymentPreference.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created PaymentPreference: {name}"))
            
            else:
                self.stdout.write(f"Already exists: {name}")
        
        self.stdout.write(self.style.SUCCESS("PaymentPreference seeding complete."))