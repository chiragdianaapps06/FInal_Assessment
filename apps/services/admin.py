from django.contrib import admin
from .models import Service, ServiceProvider

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'duration_minutes', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    list_filter = ('is_active',)

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience_years', 'is_available', 'rating')
    search_fields = ('user__username',)
    list_filter = ('is_available',)
    filter_horizontal = ('services',)
