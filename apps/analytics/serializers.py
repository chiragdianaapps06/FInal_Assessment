from rest_framework import serializers
from .models import DailyBookingMetrics

class DailyBookingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyBookingMetrics
        fields = '__all__'
