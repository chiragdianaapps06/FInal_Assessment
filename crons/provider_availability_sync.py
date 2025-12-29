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

from apps.services.models import ServiceProvider
from apps.activity_logs.utils import create_activity_log

def sync_provider_availability():
    threshold = timezone.now() - timedelta(hours=24)
    
    # Find providers who were active (updated) more than 24 hours ago and are still marked as available
    inactive_providers = ServiceProvider.objects.filter(
        is_available=True,
        updated_at__lt=threshold
    )
    
    count = inactive_providers.count()
    provider_ids = list(inactive_providers.values_list('id', flat=True))
    
    # Mark them as unavailable
    inactive_providers.update(is_available=False, updated_at=timezone.now())
    
    if count > 0:
        # Log the updates
        create_activity_log(
            user=None,
            action="Provider Availability Sync",
            entity_type="ServiceProvider",
            details={
                "inactivated_count": count,
                "provider_ids": provider_ids,
                "reason": "No activity in 24 hours"
            }
        )
        print(f"Successfully marked {count} providers as unavailable due to inactivity.")
    else:
        print("No inactive providers found.")

if __name__ == "__main__":
    sync_provider_availability()
