from rest_framework import serializers
from .models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True, allow_null=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'user_id', 'username', 'action', 'entity_type', 'entity_id', 
                  'details', 'ip_address', 'user_agent', 'timestamp']
        read_only_fields = ['timestamp']
