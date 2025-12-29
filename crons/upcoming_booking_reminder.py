import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()

from apps.bookings.models import Booking
from apps.activity_logs.utils import create_activity_log

def upcoming_booking_reminder():
    now = timezone.now()
    next_24_hours = now + timedelta(hours=24)
    
    # Find bookings scheduled within the next 24 hours that are not cancelled or completed
    upcoming_bookings = Booking.objects.filter(
        scheduled_date__range=(now, next_24_hours),
        status__in=['pending', 'confirmed', 'in_progress']
    )
    
    count = upcoming_bookings.count()
    
    # Log the reminder count
    create_activity_log(
        user=None,
        action="Upcoming Booking Reminder",
        entity_type="Booking",
        entity_id=str(upcoming_bookings.first().id),
        details={
            "upcoming_count": count,
            "time_window": "Next 24 hours"
        }
    )
    
    print(f"Reminder: There are {count} upcoming bookings in the next 24 hours.")

if __name__ == "__main__":
    upcoming_booking_reminder()
