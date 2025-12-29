from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
