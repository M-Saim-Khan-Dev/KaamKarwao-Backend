import pika
import json
from django.conf import settings

def publish_location_updated(location):
    connection= pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel= connection.channel()

    channel.exchange_declare(exchange='location_events', exchange_type='fanout', durable=True)

    payload = {
        "event": "location.updated",
        "location_id": location.id,
        "data": 
        {
            "house_number": location.house_number,
            "street_number": location.street_number,
            "landmark": location.landmark,
            "zip_code": location.zip_code,
            "city_id": location.city_id,
            "area_id": location.area_id,
            "country_id": location.country_id
        },
    }
    channel.basic_publish(
        exchange='location_events',
        routing_key='',
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2, content_type='application/json'),

    )
    connection.close()