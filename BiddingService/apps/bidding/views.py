from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Bid
from .serializers import BidSerializer
# Create your views here.

class ListBidsByTaskView(generics.ListAPIView):
    serializer_class= BidSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return Bid.objects.filter(task_id=task_id, deleted_at__isnull=True)