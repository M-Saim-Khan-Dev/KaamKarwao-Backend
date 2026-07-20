from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateLocationView,CreateCountryView, CreateCityView, CreateAreaView
from rest_framework.routers import DefaultRouter

router  = DefaultRouter()
router.register('areas', CreateAreaView)
router.register('cities', CreateCityView)
router.register('countries', CreateCountryView)
router.register('locations', CreateLocationView)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + router.urls