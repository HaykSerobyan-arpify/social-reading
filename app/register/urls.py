from django.urls import include, path
from rest_framework import routers
from register.views import UsersViewSet

router = routers.DefaultRouter()
router.register('', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
