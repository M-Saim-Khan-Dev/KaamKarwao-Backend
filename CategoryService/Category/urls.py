from rest_framework.routers import DefaultRouter
from .views import CategoryView
router  = DefaultRouter()
router.register('category', CategoryView)
urlpatterns=router.urls