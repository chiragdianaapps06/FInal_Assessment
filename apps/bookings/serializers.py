from rest_framework import serializers
from .models import Booking
from apps.services.models import Service, ServiceProvider

class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    service_name = serializers.ReadOnlyField(source='service.name')
    provider_name = serializers.ReadOnlyField(source='provider.user.username')

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_number', 'customer', 'customer_name', 'provider', 
            'provider_name', 'service', 'service_name', 'status', 
            'scheduled_date', 'total_amount', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['booking_number', 'customer', 'total_amount', 'created_at', 'updated_at', 'completed_at']

    def validate(self, data):
        provider = data.get('provider')
        if provider and not provider.is_available:
            raise serializers.ValidationError("The selected service provider is currently unavailable.")
        return data

class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']
