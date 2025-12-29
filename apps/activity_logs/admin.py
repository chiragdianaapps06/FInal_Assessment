from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'action', 'entity_type', 'entity_id', 'ip_address', 'timestamp')
    list_filter = ('action', 'entity_type', 'timestamp')
    search_fields = ('username', 'action', 'entity_type', 'entity_id', 'ip_address')
    readonly_fields = ('user', 'username', 'action', 'entity_type', 'entity_id', 
                       'details', 'ip_address', 'user_agent', 'timestamp')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
