"""
import pika
import json
from django.conf import settings

def setup_channel(channel):
    channel.exchange_declare(exchange='location_events', exchange_type='fanout', durable=True)
    channel.queue_declare(queue='user_service_location_updates', durable= True)
    channel.queue_bind(exchange='location_events', queue='user_service_location_updates')

def handle_location_updated(event_data):
    from .models import User
    location_id = event_data["location_id"]
    zip_code = event_data["data"]["zip_code"]
    updated = User.objects.filter(location_id=location_id).update(location_zip_code = zip_code)
    print(f"location.updated recieved for location_id={location_id}, updated {updated} user(s)")

def callback(ch,method,properties,body):
    try:
        event=json.loads(body)
        if event["event"] == "location.updated":
            handle_location_updated(event)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process message {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consuming():
    connection= pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel=connection.channel()
    setup_channel(channel)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="user_service_location_updates", on_message_callback=callback)
    print("Waiting for location events. To exit press CTRL+C")
    channel.start_consuming()
    """