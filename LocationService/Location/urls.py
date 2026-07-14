from .views import CreateLocationView,CreateCountryView, CreateCityView, CreateAreaView
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()
router.register('areas', CreateAreaView)
router.register('cities', CreateCityView)
router.register('countries', CreateCountryView)
router.register('locations', CreateLocationView)
urlpatterns=router.urls