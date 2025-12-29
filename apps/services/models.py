from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    services = models.ManyToManyField(Service, related_name='providers')
    experience_years = models.IntegerField()
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Provider: {self.user.username}"
