from rest_framework.routers import SimpleRouter
from .views import IncomeViewSet, IncomesGroupViewSet


router = SimpleRouter()
router.register('groups', IncomesGroupViewSet, basename='incgroups')
router.register('', IncomeViewSet, basename='incomes')
urlpatterns = router.urls