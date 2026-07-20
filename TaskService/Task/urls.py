from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateTaskView,GetTaskByCreatedByView
router  = DefaultRouter()
router.register('task_service', CreateTaskView)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('task_service/customer/<int:created_by>/', GetTaskByCreatedByView.as_view(), name='tasks-by-creator'),
] + router.urls