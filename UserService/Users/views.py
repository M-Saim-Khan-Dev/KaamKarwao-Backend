from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .serializers import UserSerializer,UpdateImageSerializer,UpdateUserIsVerifiedSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["is_verified"] = user.is_verified
    refresh["is_staff"] = user.is_staff 
    return refresh

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes=[AllowAny]
    
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
        
        refresh = get_tokens_for_user(user)
        serializer = UserSerializer(user)
        return Response({
            "user": serializer.data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
class UpdateUserImageView(generics.UpdateAPIView):
    serializer_class = UpdateImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
class UpdateUserVerifiedView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserIsVerifiedSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, id=pk)