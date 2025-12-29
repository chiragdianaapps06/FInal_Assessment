from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from apps.bookings.models import Booking
from apps.services.models import Service, ServiceProvider
from django.contrib.auth.models import User
from .models import DailyBookingMetrics
from rest_framework import status

class DashboardAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        
        # Total bookings
        total_bookings = Booking.objects.count()
        completed_bookings = Booking.objects.filter(status='completed').count()
        cancelled_bookings = Booking.objects.filter(status='cancelled').count()
        
        # Total revenue (from completed bookings)
        total_revenue = Booking.objects.filter(status='completed').aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Active customers (users with at least one booking)
        active_customers = User.objects.filter(bookings__isnull=False).distinct().count()
        
        # Active providers (is_available=True)
        active_providers = ServiceProvider.objects.filter(is_available=True).count()
        
        # Today's bookings
        today_bookings = Booking.objects.filter(
            created_at__date=today
        ).count()
        
        # Today's revenue
        today_revenue = Booking.objects.filter(
            created_at__date=today,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        return Response({
            "message": "Dashboard analytics retrieved successfully",
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_revenue": str(total_revenue),
            "active_customers": active_customers,
            "active_providers": active_providers,
            "today_bookings": today_bookings,
            "today_revenue": str(today_revenue)
        }, status=status.HTTP_200_OK)



class BookingStatusAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        status_breakdown = Booking.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return Response({
            'message': 'Booking status analytics retrieved successfully',
            'data': list(status_breakdown)
        }, status=status.HTTP_200_OK)



class TopBookedServicesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        top_services = Service.objects.annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:limit]
        
        data = [
            {
                "id": service.id,
                "name": service.name,
                "booking_count": service.booking_count,
                "base_price": str(service.base_price)
            }
            for service in top_services
        ]
        
        return Response({
            'message': 'Top booked services retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)



class RevenueAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Get period parameter (default: last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now().date() - timedelta(days=days)
        
        # Daily revenue breakdown
        daily_revenue = Booking.objects.filter(
            created_at__date__gte=start_date,
            status='completed'
        ).values('created_at__date').annotate(
            revenue=Sum('total_amount'),
            count=Count('id')
        ).order_by('created_at__date')
        
        # Total revenue in period
        total_revenue = Booking.objects.filter(
            created_at__date__gte=start_date,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        return Response({
            "message": "Revenue analytics retrieved successfully",
            "period_days": days,
            "total_revenue": str(total_revenue),
            "daily_breakdown": [
                {
                    "date": str(item['created_at__date']),
                    "revenue": str(item['revenue']),
                    "bookings": item['count']
                }
                for item in daily_revenue
            ]
        }, status=status.HTTP_200_OK)



class ProviderPerformanceView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        providers = ServiceProvider.objects.annotate(
            total_bookings=Count('bookings'),
            completed_bookings=Count('bookings', filter=Q(bookings__status='completed')),
            total_revenue=Sum('bookings__total_amount', filter=Q(bookings__status='completed'))
        ).order_by('-total_bookings')
        
        data = [
            {
                "id": provider.id,
                "username": provider.user.username,
                "total_bookings": provider.total_bookings,
                "completed_bookings": provider.completed_bookings,
                "total_revenue": str(provider.total_revenue or 0),
                "rating": str(provider.rating),
                "is_available": provider.is_available
            }
            for provider in providers
        ]
        
        return Response({
            'message': 'Provider performance analytics retrieved successfully',
            'data': data
        }, status=status.HTTP_200_OK)

