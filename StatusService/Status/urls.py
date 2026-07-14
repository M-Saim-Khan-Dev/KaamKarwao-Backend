from rest_framework.routers import DefaultRouter
from .views import CreateStatusView
router  = DefaultRouter()
router.register('status', CreateStatusView)
urlpatterns=router.urls