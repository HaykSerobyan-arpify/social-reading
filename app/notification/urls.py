from django.urls import path
from rest_framework import routers
from .views import NotificationViewSet

router = routers.DefaultRouter()
router.register('', NotificationViewSet)

urlpatterns = router.urls