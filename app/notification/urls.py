from django.urls import path
from .views import showNotifications

urlpatterns = [
    path('', showNotifications, name='show-notifications'),
]
