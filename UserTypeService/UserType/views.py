from django.shortcuts import render,get_object_or_404
from .serializers import UserTypeSerializer
from .models import UserType
from rest_framework.permissions import IsAdminUser,IsAuthenticated, AllowAny
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema,extend_schema_view

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List UserTypes", description="Returns UserTypes"),
    create=extend_schema(summary="Create UserTypes by Admin Users"),
    retrieve= extend_schema(summary="Get a particular UserType"),
    update=extend_schema(summary="Fully Update UserTypes"),
    partial_update=extend_schema(summary="Partially Update UserTypes"),
    destroy=extend_schema(summary="Delete UserTypes"),
)

class CreateUserTypeView(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]