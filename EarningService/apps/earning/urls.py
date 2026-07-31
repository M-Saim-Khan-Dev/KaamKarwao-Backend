from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateWorkerEarningView,InternalAddEarningView
router  = DefaultRouter()
router.register('earnings', CreateWorkerEarningView, basename='earnings')
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('earnings/internal/add/', InternalAddEarningView.as_view(), name='internal-add-earning'),
] + router.urls