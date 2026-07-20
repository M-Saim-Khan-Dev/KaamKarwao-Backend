from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateAttachmentView,GetAttachmentByTaskView
router  = DefaultRouter()
router.register('attachment_service', CreateAttachmentView)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('attachment_service/<int:task_id>/', GetAttachmentByTaskView.as_view(), name='attachment-via-taskid'),
] + router.urls