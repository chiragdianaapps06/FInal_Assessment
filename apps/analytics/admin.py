from django.contrib import admin
from .models import DailyBookingMetrics

@admin.register(DailyBookingMetrics)
class DailyBookingMetricsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_bookings', 'completed_bookings', 'cancelled_bookings', 'total_revenue')
    list_filter = ('date',)
    search_fields = ('date',)
    readonly_fields = ('created_at',)
