from rest_framework import routers
from .views import QuotesViewSet

router = routers.SimpleRouter()
router.register('', QuotesViewSet)

urlpatterns = router.urls
