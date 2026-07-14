from .views import ConfigurationView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('configuration', ConfigurationView)
urlpatterns = router.urls