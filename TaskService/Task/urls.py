from rest_framework.routers import DefaultRouter
from .views import CreateTaskView
router  = DefaultRouter()
router.register('task', CreateTaskView)
urlpatterns=router.urls