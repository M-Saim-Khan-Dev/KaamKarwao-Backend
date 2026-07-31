"""
ASGI config for BiddingService project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
import apps.bidding.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(apps.bidding.routing.websocket_urlpatterns),
})
