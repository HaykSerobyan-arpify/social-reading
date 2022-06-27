# chat/urls.py
from django.urls import path

from . import views
from .consumers import ChatConsumer

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path("<slug>/", ChatConsumer.as_asgi())
]
