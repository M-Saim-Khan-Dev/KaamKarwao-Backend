from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .serializers import UserTypeSerializer,UserSerializer,UpdateImageSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserType, User
# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes=[AllowAny]

class SearchUserByPhoneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, phone_number):
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        user=get_object_or_404(User, phone_number=phone_number)
        return Response({
            "id": user.id,
            "user_type": user.user_type.name if user.user_type else None,
            "location_id": user.location_id,
            "location_zip_code": user.location_zip_code,
        })

class CreateUserTypeView(generics.CreateAPIView):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    permission_classes = [IsAdminUser]

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UpdateUserImageView(generics.UpdateAPIView):
    serializer_class = UpdateImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user