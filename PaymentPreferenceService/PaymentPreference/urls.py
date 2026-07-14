from rest_framework.routers import DefaultRouter
from .views import CreatePaymentPreferenceView
router  = DefaultRouter()
router.register('paymentpref', CreatePaymentPreferenceView)
urlpatterns=router.urls