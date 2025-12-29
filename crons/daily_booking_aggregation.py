import os
import sys
import django
from django.utils import timezone
from django.db.models import Count, Sum

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()

from apps.bookings.models import Booking
from apps.analytics.models import DailyBookingMetrics
from apps.activity_logs.utils import create_activity_log

def aggregate_daily_bookings():
    today = timezone.now().date()
    
    # Aggregate data for today
    metrics = Booking.objects.filter(created_at__date=today).aggregate(
        total_bookings=Count('id'),
        completed_bookings=Count('id', filter=django.db.models.Q(status='completed')),
        cancelled_bookings=Count('id', filter=django.db.models.Q(status='cancelled')),
        total_revenue=Sum('total_amount', filter=django.db.models.Q(status='completed'))
    )
    
    total_bookings = metrics['total_bookings'] or 0
    completed_bookings = metrics['completed_bookings'] or 0
    cancelled_bookings = metrics['cancelled_bookings'] or 0
    total_revenue = metrics['total_revenue'] or 0
    
    # Update or create DailyBookingMetrics
    obj, created = DailyBookingMetrics.objects.update_or_create(
        date=today,
        defaults={
            'total_bookings': total_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_revenue': total_revenue
        }
    )
    
    summary = f"Aggregated {total_bookings} bookings. Revenue: {total_revenue}"
    
    # Log the aggregation summary
    create_activity_log(
        user=None,
        action="Daily Booking Aggregation",
        entity_type="Analytics",
        entity_id=str(obj.id),
        details={
            "date": str(today),
            "total_bookings": total_bookings,
            "completed_bookings": completed_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_revenue": str(total_revenue)
        }
    )
    
    print(f"Successfully aggregated metrics for {today}: {summary}")

if __name__ == "__main__":
    aggregate_daily_bookings()
