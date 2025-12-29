from .models import ActivityLog

def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def create_activity_log(user, action, entity_type, entity_id=None, details=None, request=None):
    """
    Helper function to create activity logs.
    
    Args:
        user: User object (can be None for anonymous actions)
        action: String describing the action performed
        entity_type: Type of entity being acted upon
        entity_id: ID of the entity (optional)
        details: Additional details as dict (optional)
        request: HTTP request object (optional)
    """
    username = user.username if user else "Anonymous"
    ip_address = get_client_ip(request) if request else None
    user_agent = request.META.get('HTTP_USER_AGENT', '') if request else None
    
    ActivityLog.objects.create(
        user=user,
        username=username,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id) if entity_id else None,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
