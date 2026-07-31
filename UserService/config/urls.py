"""
URL configuration for UserService project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import CreateUserView,UpdateUserView,UpdateUserImageView,UserLoginView,UpdateUserVerifiedView,GetUserInfoView,DeleteUserView,InternalUpdateRatingView,AdminListUsersView,AdminUpdateUserView,AdminDeleteUserView,CheckPhoneNumberView,AdminListUnverifiedUsersView,SubmitVerificationAttachmentsView,InternalUserStatusView
urlpatterns = [
    path('app/admin/', admin.site.urls),
    path("app/register/user/",CreateUserView.as_view(),name = 'register'),
    path("app/user/token/",TokenObtainPairView.as_view(),name = 'get_token'),
    path("app/user/token/refresh/",TokenRefreshView.as_view(),name = 'refresh-token'),
    path('app/user/update/', UpdateUserView.as_view(), name='update-user'),
    path('app/user/delete/', DeleteUserView.as_view(), name='delete-user'),
    path('app/user/update/image/', UpdateUserImageView.as_view(), name='update-image'),
    path('app/user/verification-attachments/', SubmitVerificationAttachmentsView.as_view(), name='submit-verification-attachments'),
    path('app/user/login/', UserLoginView.as_view(), name='login'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('app/user/info/<int:pk>/', GetUserInfoView.as_view(), name='user-info'),
    path('app/user/<int:user_id>/rating/internal/', InternalUpdateRatingView.as_view(), name='internal-update-rating'),
    path('administrator/get/users/', AdminListUsersView.as_view(), name='admin-list-users'),
    path('administrator/get/users/<int:pk>/', AdminUpdateUserView.as_view(), name='admin-update-user'),
    path('administrator/get/users/<int:pk>/delete/', AdminDeleteUserView.as_view(), name='admin-delete-user'),
    path('administrator/unverified/', AdminListUnverifiedUsersView.as_view(), name='admin-unverified-users'),
    path('administrator/verify/<int:pk>/', UpdateUserVerifiedView.as_view(), name='update-user-verified'),
    path('app/user/check-phone/', CheckPhoneNumberView.as_view(), name='check-phone'),
    path('internal/user/<int:user_id>/status/', InternalUserStatusView.as_view()),

]
