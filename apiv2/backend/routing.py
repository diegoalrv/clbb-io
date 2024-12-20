from django.urls import re_path
from . import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

# websocket_urlpatterns = [
#     re_path(r'ws/chat/$', consumers.MyWebSocketConsumer.as_asgi()),  # Ruta WebSocket
# ]
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', consumers.MyWebSocketConsumer.as_asgi()),
    ])
})