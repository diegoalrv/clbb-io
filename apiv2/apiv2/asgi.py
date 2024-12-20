"""
ASGI config for apiv2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from backend.routing import application  # Asegúrate de importar las rutas de WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apiv2.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Manejo de solicitudes HTTP tradicionales
    "websocket": AuthMiddlewareStack(  # Manejo de conexiones WebSocket
        URLRouter(
            application  # Aquí se definen las rutas WebSocket
        )
    ),
})

