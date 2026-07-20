from django.shortcuts import render
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from django.utils import timezone
from drf_spectacular.utils import extend_schema,extend_schema_view
from django.db.models import Avg

# Create your views here.

@extend_schema_view(
    list = extend_schema(summary="List Reviews", description="Returns NonDeleted Reviews for the All users"),
    create=extend_schema(summary="Create Reviews by Authenticated Users"),
    retrieve= extend_schema(summary="Get one particular Review"),
    update=extend_schema(summary="Fully Update Reviews"),
    partial_update=extend_schema(summary="Partially Update Reviews"),
    destroy=extend_schema(summary="Soft-delete Reviews, setting deleted time to now"),
)

class CreateReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.filter(deleted_at__isnull=True)
    serializer_class = ReviewSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

@extend_schema(
        summary="Gets the number of Reviews a User has gotten",
    )
class GetUserReviewCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        count = Review.objects.filter(user_id=user_id, deleted_at__isnull=True).count()
        return Response({"user_id": user_id, "review_count": count})
    
@extend_schema(
        summary="Gives User Rating According to Reviews (5 if 0 reviews)",
    )
class GetUserRatingView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,user_id):
        average_rating = Review.objects.filter(
            user_id=user_id, deleted_at__isnull=True
            ).aggregate(avg=Avg('rating'))['avg']
        if average_rating is None:
            average_rating = 5
        
        return Response({"average_rating": round(average_rating, 2)})