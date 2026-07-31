from django.core.management.base import BaseCommand
from Users.consumer import start_consuming

class Command(BaseCommand):
    help = "Consumes location.updated events from RabbitMQ"

    def handle(self, *args, **options):
        start_consuming()