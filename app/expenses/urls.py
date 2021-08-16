from rest_framework.routers import SimpleRouter
from .views import ExpensesGroupViewSet, ExpenseViewSet


router = SimpleRouter()
router.register('groups', ExpensesGroupViewSet, basename='expgroups')
router.register('', ExpenseViewSet, basename='expenses')
urlpatterns = router.urls