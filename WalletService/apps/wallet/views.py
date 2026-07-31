from django.shortcuts import render
from .serializers import WalletSerializer
from .models import Wallet
from rest_framework.permissions import IsAuthenticated,AllowAny, IsAdminUser
from rest_framework import viewsets,status
from drf_spectacular.utils import extend_schema,extend_schema_view
from rest_framework.response import Response
# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Wallet's info"),
    create=extend_schema(summary="Create Wallet for Authenticated Users"),
    retrieve= extend_schema(summary="Get one user's Wallet"),
    update=extend_schema(summary="Fully Update Wallet"),
    partial_update=extend_schema(summary="Partially Update Wallet"),
    destroy=extend_schema(summary="Soft Delete Wallet"),
)

class CreateWalletView(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    lookup_field = 'user_id'

    def get_permissions(self):
        if self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        if self.request.headers.get('X-Is-Staff') == 'true':
            return Wallet.objects.all()
        user_id = self.request.headers.get('X-User-Id')
        return Wallet.objects.filter(user_id=user_id)
    
    def create(self,request,*args,**kwargs):
        user_id = request.headers.get('X-User-Id')

        if Wallet.objects.filter(user_id=user_id).exists():
            return Response(
                {"error": "Wallet record already exists for this User"},
                status=status.HTTP_409_CONFLICT,
            )
        wallet = Wallet.objects.create(user_id=user_id)
        return Response(WalletSerializer(wallet).data, status=status.HTTP_201_CREATED)