from rest_framework.routers import SimpleRouter
from .views import SourceViewSet


router = SimpleRouter()
router.register('', SourceViewSet, basename='sources')
urlpatterns = router.urls