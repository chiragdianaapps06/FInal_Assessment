from django.urls import path
from .views import (
    DashboardAnalyticsView,
    BookingStatusAnalyticsView,
    TopBookedServicesView,
    RevenueAnalyticsView,
    ProviderPerformanceView
)

urlpatterns = [
    path('analytics/dashboard/', DashboardAnalyticsView.as_view(), name='analytics-dashboard'),
    path('analytics/bookings/status/', BookingStatusAnalyticsView.as_view(), name='analytics-booking-status'),
    path('analytics/services/top-booked/', TopBookedServicesView.as_view(), name='analytics-top-services'),
    path('analytics/revenue/', RevenueAnalyticsView.as_view(), name='analytics-revenue'),
    path('analytics/providers/performance/', ProviderPerformanceView.as_view(), name='analytics-provider-performance'),
]
