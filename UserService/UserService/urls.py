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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Users.views import CreateUserView,CreateLocationView,CurrentUserView, CreateUserTypeView, CreateCountryView, CreateCityView, CreateAreaView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("app/register/user/",CreateUserView.as_view(),name = 'register'),
    path("app/user/token/",TokenObtainPairView.as_view(),name = 'get_token'),
    path("app/user/token/refresh/",TokenRefreshView.as_view(),name = 'refresh-token'),
    path('app/register/location/', CreateLocationView.as_view(), name='create-location'),
    path('app/register/user_type/', CreateUserTypeView.as_view(), name='create-type'),
    path('app/register/area/', CreateAreaView.as_view(), name='create-area'),
    path('app/register/city/', CreateCityView.as_view(), name='create-city'),
    path('app/register/country/', CreateCountryView.as_view(), name='create-country'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    
]
