from .serializers import WorkerEarningsSerializer
from .models import WorkerEarnings
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema,extend_schema_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
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
    lookup_field = 'worker_id'

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        if self.request.headers.get('X-Is-Staff') == 'true':
            return WorkerEarnings.objects.all()
        worker_id = self.request.headers.get('X-User-Id')
        return WorkerEarnings.objects.filter(worker_id=worker_id)
    
    def create(self,request,*args,**kwargs):
        worker_id = request.headers.get('X-User-Id')

        if WorkerEarnings.objects.filter(worker_id=worker_id).exists():
            return Response(
                {"error": "Earnings record already exists for this worker"},
                status=status.HTTP_409_CONFLICT,
            )
        earning = WorkerEarnings.objects.create(worker_id=worker_id)
        return Response(WorkerEarningsSerializer(earning).data, status=status.HTTP_201_CREATED)

@extend_schema(exclude=True)
class InternalAddEarningView(APIView):
    permission_classes = [AllowAny]

    def post (self, request):
        worker_id = request.data.get("worker_id")
        price = request.data.get("price")

        if not worker_id or price is None:
            return Response({"error": "worker_id and price are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            earning = WorkerEarnings.objects.get(worker_id=worker_id)
        
        except WorkerEarnings.DoesNotExist:
            return Response({"error": f"No earnings record found for worker_id={worker_id}"}, status=status.HTTP_404_NOT_FOUND)
        
        earning.daily_earning = F('daily_earning') + price
        earning.weekly_earning=F('weekly_earning') + price
        earning.total_earning = F('total_earning') + price
        earning.daily_jobs_done = F('daily_jobs_done') + 1
        earning.total_jobs_done = F('total_jobs_done') + 1
        earning.save()
        earning.refresh_from_db()

        return Response({
            "worker_id": earning.worker_id,
            "daily_earning": earning.daily_earning,
            "weekly_earning": earning.weekly_earning,
            "total_earning": earning.total_earning,
            "daily_jobs_done": earning.daily_jobs_done,
            "total_jobs_done": earning.total_jobs_done,
        }, status=status.HTTP_200_OK)
