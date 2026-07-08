from django.shortcuts import render,get_object_or_404
from .serializers import UserTypeSerializer
from .models import UserType
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
class CreateUserTypeView(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]