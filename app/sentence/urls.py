from rest_framework import routers
from .views import SentenceViewSet

router = routers.DefaultRouter()
router.register('', SentenceViewSet)

urlpatterns = router.urls
