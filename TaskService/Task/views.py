from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
# Create your views here.
class CreateTaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def get_permissions(self):
        return [IsAuthenticated()]