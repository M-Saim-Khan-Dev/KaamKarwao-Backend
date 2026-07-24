from .serializers import CategorySerializer,SubCategorySerializer
from .models import Category,SubCategory
from django.utils import timezone
from rest_framework.permissions import IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema,extend_schema_view
from rest_framework import viewsets
# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Categories", description="Returns Categories for the All users"),
    create=extend_schema(summary="Create Categories for Authenticated Users"),
    retrieve= extend_schema(summary="Get specific Category"),
    update=extend_schema(summary="Fully Update Categories (Authenticated)"),
    partial_update=extend_schema(summary="Partially Update Categories (Authenticated)"),
    destroy=extend_schema(summary="Delete Categories "),
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
@extend_schema_view(
    list = extend_schema(summary="List Categories", description="Returns Categories for the All users"),
    create=extend_schema(summary="Create Categories for Authenticated Users"),
    retrieve= extend_schema(summary="Get specific Category"),
    update=extend_schema(summary="Fully Update Categories (Authenticated)"),
    partial_update=extend_schema(summary="Partially Update Categories (Authenticated)"),
    destroy=extend_schema(summary="Delete Categories "),
)

class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]