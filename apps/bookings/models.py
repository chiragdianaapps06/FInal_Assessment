from django.db import models
from django.contrib.auth.models import User
from apps.services.models import Service, ServiceProvider
from django.utils import timezone
import random
import string

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_number = models.CharField(max_length=50, unique=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    provider = models.ForeignKey(ServiceProvider, null=True, on_delete=models.SET_NULL, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.booking_number:
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            self.booking_number = f"BK-{date_str}-{random_str}"
        
        if not self.total_amount and self.service:
            self.total_amount = self.service.base_price
            
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.booking_number
