# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path("chats/<conversation_name>/", consumers.ChatConsumer.as_asgi()),
    re_path("notifications/", consumers.NotificationConsumer.as_asgi()),
]
