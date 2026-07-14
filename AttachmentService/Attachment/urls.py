from rest_framework.routers import DefaultRouter
from .views import CreateAttachmentView
router  = DefaultRouter()
router.register('attachment', CreateAttachmentView)
urlpatterns=router.urls