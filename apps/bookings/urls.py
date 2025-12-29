from django.urls import path
from .views import BookingViewSet

booking_list = BookingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
booking_detail = BookingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
booking_status = BookingViewSet.as_view({
    'patch': 'update_status'
})
booking_admin_all = BookingViewSet.as_view({
    'get': 'admin_all_bookings'
})

urlpatterns = [
    path('bookings/', booking_list, name='booking-list'),
    path('bookings/admin/all/', booking_admin_all, name='booking-admin-all'),
    path('bookings/<int:pk>/', booking_detail, name='booking-detail'),
    path('bookings/<int:pk>/status/', booking_status, name='booking-status'),
]
