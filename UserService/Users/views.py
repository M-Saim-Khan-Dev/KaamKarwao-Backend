from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from rest_framework import generics, status
from .serializers import UserSerializer,UpdateImageSerializer,UpdateUserIsVerifiedSerializer,UserInfoSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .supabase_client import upload_to_supabase
from rest_framework.parsers import MultiPartParser, FormParser
from .pagination import StandardResultsPagination

# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["is_verified"] = user.is_verified
    refresh["is_staff"] = user.is_staff 
    refresh["usertype_id"] = user.usertype_id
    return refresh

@extend_schema(
        summary="Create a User",
        description="Creates the User Using a valid locationid and sets the user to be verified",
    )
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class= UserSerializer    
    permission_classes=[AllowAny]
    
@extend_schema(
        summary="Logs in a User",
        description="Logs in the User Using a valid Phone number and Password",
    )
    
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

@extend_schema(
        summary="Updates a User",
        description="Updates any field of the User",
    )

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
@extend_schema(
        summary="Updates the User Profile Picture",
    )


class UpdateUserImageView(generics.UpdateAPIView):
    serializer_class = UpdateImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)
    
    def update(self,request, *args,**kwargs):
        instance= self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial = True)
        serializer.is_valid(raise_exception= True)

        file = serializer.validated_data["file"]
        url= upload_to_supabase(file)

        instance.image=url
        instance.save()
        return Response(UpdateImageSerializer(instance).data, status=status.HTTP_200_OK)
    
@extend_schema(
        summary="Updates the User Verification",
    )


class UpdateUserVerifiedView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True) 
    serializer_class = UpdateUserIsVerifiedSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, id=pk)

@extend_schema(
        summary="Soft-Deletes a User",
        description="Deletes a User by setting deleted at to now",
    )    

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.is_active = False
        instance.save()

@extend_schema(
        summary="Get all user info using user_id",
    )

class GetUserInfoView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

@extend_schema(
    summary="List all users (Admin only)",
    description="Returns a paginated list of all non-deleted users. Admin access required.",
)
class AdminListUsersView(generics.ListAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    serializer_class = UserInfoSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsPagination

@extend_schema(
    summary="Update any user's profile (Admin only)",
    description="Allows an admin to update any user's profile by user ID.",
)
class AdminUpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

@extend_schema(
    summary="Soft-delete any user's profile (Admin only)",
    description="Allows an admin to soft-delete any user by ID, recording who deleted them.",
)
class AdminDeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.is_active = False
        instance.deleted_by = self.request.user
        instance.save()

@extend_schema(exclude=True)
class InternalUpdateRatingView(APIView):
    permission_classes= [AllowAny]

    def patch(self,request,user_id):
        overall_rating = request.data.get("overall_rating")
        if overall_rating is None:
            return Response({"error": "overall_rating is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=user_id)
        user.overall_rating = overall_rating
        user.save()
        return Response({"id": user.id, "overall_rating": user.overall_rating}, status=status.HTTP_200_OK)