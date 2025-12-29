from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'customer', 'service', 'status', 'scheduled_date', 'total_amount')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('booking_number', 'customer__username', 'service__name')
    readonly_fields = ('booking_number', 'total_amount', 'created_at', 'updated_at', 'completed_at')
