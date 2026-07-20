from .serializers import CategorySerializer
from .models import Category
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated, AllowAny
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
        return [IsAuthenticated()] # make this IsAdmin in the future