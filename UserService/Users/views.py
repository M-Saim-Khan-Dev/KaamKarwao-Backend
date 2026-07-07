from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import generics, status
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
    
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post (self, request):
        phone_number = request.data.get('phone_number')
        password= request.data.get('password')

        if not phone_number or not password:
            return Response({"error": "Phone number and Password is Required"}, status=status.HTTP_400_BAD_REQUEST)

        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"error": "Invalid Credentials"}, status= status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.deleted_at is not None:
            return Response({"error": "This account has been deleted"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "This account is inactive"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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