from rest_framework import routers
from .views import SaveViewSet

router = routers.DefaultRouter()
router.register('', SaveViewSet)

urlpatterns = router.urls
