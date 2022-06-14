from django.urls import include, path
from rest_framework import routers
from library.views import BookViewSet

router = routers.DefaultRouter()
router.register('', BookViewSet)

urlpatterns = [path('', include(router.urls))]
