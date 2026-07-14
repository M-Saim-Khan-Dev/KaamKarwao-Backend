from .serializers import StatusSerializer
from .models import Status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
# Create your views here.
class CreateStatusView(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    def get_permissions(self):
        return [IsAuthenticated()]