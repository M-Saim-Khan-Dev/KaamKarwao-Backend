from rest_framework.routers import DefaultRouter
from .views import CreateUserTypeView
router  = DefaultRouter()
router.register('usertype', CreateUserTypeView)
urlpatterns=router.urls