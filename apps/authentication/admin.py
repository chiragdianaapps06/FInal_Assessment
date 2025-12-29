from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'user_type', 'created_at')
    search_fields = ('user__username', 'phone', 'city')
    list_filter = ('user_type', 'city')
