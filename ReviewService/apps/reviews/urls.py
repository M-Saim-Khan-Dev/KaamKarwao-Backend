from django.urls import path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateReviewView,GetUserReviewCountView,GetUserRatingView
router  = DefaultRouter()
router.register('review_service', CreateReviewView)
urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('review_service/customer/<int:user_id>/', GetUserReviewCountView.as_view(), name='user-review-count'),
    path('review_service/rating/<int:user_id>/', GetUserRatingView.as_view(), name='user-rating'),
] + router.urls