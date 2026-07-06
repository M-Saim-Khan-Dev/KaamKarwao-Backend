from django.shortcuts import render
from rest_framework import generics
from .serializers import AreaSerializer, CountrySerializer, CitySerializer,UserTypeSerializer,LocationSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserType, Area, City, Country, Location, User
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes=[AllowAny]

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user = request.user
        return Response({
        "id": user.id,
        "user_type": user.user_type.name if user.user_type else None
    })
    
class CreateLocationView(generics.CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [AllowAny]

class CreateAreaView(generics.CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = [AllowAny]

class CreateCityView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

class CreateCountryView(generics.CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CreateUserTypeView(generics.CreateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [IsAdminUser]