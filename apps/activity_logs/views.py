from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ActivityLog
from .serializers import ActivityLogSerializer
from django.contrib.auth.models import User

class ActivityLogCreateView(generics.CreateAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActivityLogListView(generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtering options
        action = self.request.query_params.get('action', None)
        entity_type = self.request.query_params.get('entity_type', None)
        username = self.request.query_params.get('username', None)
        
        if action:
            queryset = queryset.filter(action__icontains=action)
        if entity_type:
            queryset = queryset.filter(entity_type__icontains=entity_type)
        if username:
            queryset = queryset.filter(username__icontains=username)
        
        return queryset

class UserActivityLogView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs.get('userId')
        return ActivityLog.objects.filter(user_id=user_id)
