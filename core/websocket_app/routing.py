# websocket_app/routing.py
from django.urls import re_path
from .consumers import DashboardConsumer, MapConsumer

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', DashboardConsumer.as_asgi()),
    re_path(r'ws/map/$', MapConsumer.as_asgi()),
]
