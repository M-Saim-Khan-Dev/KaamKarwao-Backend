from django.core.management.base import BaseCommand
from Users.models import User

class Command(BaseCommand):
    help = "Seeds test users"

    def handle(self,*args,**options):
        test_users = [
            {
                "email": "testconsumer123@gmail.com",
                "password":"TestConsumer123",
                "first_name": "Test",
                "last_name":"Consumer",
                "phone_number":"+923218599844",
                "usertype_id":2,
                "location_id": 5,
                "is_verified":True,
            },
            {
                "email": "testworker123@gmail.com",
                "password":"TestWorker123",
                "first_name": "Test",
                "last_name":"Worker",
                "phone_number":"+923238599844",
                "usertype_id":3,
                "location_id": 5,
                "is_verified":True, 
            },
            {
                "email": "testadmin123@gmail.com",
                "password":"TestAdmin123",
                "first_name": "Test",
                "last_name":"Admin",
                "phone_number":"+923248599844",
                "usertype_id":1,
                "location_id": 5,
                "is_verified":True, 
            },
        ]
        
        for data in test_users:
            if User.objects.filter(email=data["email"]).exists():
                self.stdout.write(self.style.SUCCESS(f"Already Exists: {data['email']}"))
                continue
            password = data.pop("password")
            user = user.objects.create_user(email=data["email"], password=password, **{
                k: v for k, v in data.items() if k!= "email"
            })
            self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))
        
        self.stdout.write(self.style.SUCCESS("User seeding complete."))