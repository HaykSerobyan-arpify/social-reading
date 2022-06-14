from rest_framework import routers
from .views import LikeViewSet

router = routers.DefaultRouter()
router.register('', LikeViewSet)

urlpatterns = router.urls
