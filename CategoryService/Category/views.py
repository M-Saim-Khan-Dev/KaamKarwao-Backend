from .serializers import CategorySerializer
from .models import Category
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]