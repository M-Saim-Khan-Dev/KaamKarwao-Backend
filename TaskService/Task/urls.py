from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateTaskView,GetTaskByCreatedByView,GetOpenTasksView,GetTaskByWorkerView,InternalSetTaskWorkerView
router  = DefaultRouter()
router.register('task_service', CreateTaskView)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('task_service/customer/<int:created_by>/', GetTaskByCreatedByView.as_view(), name='tasks-by-creator'),
    path('task_service/open/', GetOpenTasksView.as_view(), name='open-tasks'),
    path('task_service/worker/<int:worker_id>/', GetTaskByWorkerView.as_view(), name='tasks-by-worker'),
    path('task_service/internal/<int:task_id>/set-worker/', InternalSetTaskWorkerView.as_view(), name='internal-set-worker'),
] + router.urls