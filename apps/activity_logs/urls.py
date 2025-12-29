from django.urls import path
from .views import ActivityLogCreateView, ActivityLogListView, UserActivityLogView

urlpatterns = [
    path('logs/', ActivityLogListView.as_view(), name='activity-log-list'),
    path('logs/create/', ActivityLogCreateView.as_view(), name='activity-log-create'),
    path('logs/user/<int:userId>/', UserActivityLogView.as_view(), name='user-activity-log'),
]
