import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
import store_database.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdk_main.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        store_database.routing.websocket_urls,
    )
})
