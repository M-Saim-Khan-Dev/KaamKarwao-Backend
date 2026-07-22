from .serializers import WorkerEarningsSerializer
from .models import WorkerEarnings
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Earnings", description="Returns Earnings for the Authenticated Worker users"),
    create=extend_schema(summary="Create Earnings for Authenticated Users"),
    retrieve= extend_schema(summary="Get one user's Earnings"),
    update=extend_schema(summary="Fully Update Earnings"),
    partial_update=extend_schema(summary="Partially Update Earnings"),
    destroy=extend_schema(summary="Delete Earnings"),
)

class CreateWorkerEarningView(viewsets.ModelViewSet):
    serializer_class = WorkerEarningsSerializer
    permission_classes=[IsAuthenticated]
    lookup_field = 'worker_id'
    def get_queryset(self):
        if self.request.headers.get('X-Is-Staff') == 'true':
            return WorkerEarnings.objects.all()
        worker_id = self.request.headers.get('X-User-Id')
        return WorkerEarnings.objects.filter(worker_id=worker_id)
        #in the future, make it so the frontend can update/create this and not the user themselves