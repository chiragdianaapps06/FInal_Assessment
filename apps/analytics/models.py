from django.db import models

class DailyBookingMetrics(models.Model):
    date = models.DateField(unique=True)
    total_bookings = models.IntegerField(default=0)
    completed_bookings = models.IntegerField(default=0)
    cancelled_bookings = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Daily Booking Metrics'

    def __str__(self):
        return f"Metrics for {self.date}"
