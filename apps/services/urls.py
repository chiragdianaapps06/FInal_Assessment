from django.urls import path
from .views import ServiceViewSet, ServiceProviderViewSet

service_list = ServiceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
service_detail = ServiceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
service_search = ServiceViewSet.as_view({
    'get': 'search_services'
})

provider_list = ServiceProviderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
provider_detail = ServiceProviderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('services/', service_list, name='service-list'),
    path('services/search/', service_search, name='service-search'),
    path('services/<int:pk>/', service_detail, name='service-detail'),
    
    path('providers/', provider_list, name='provider-list'),
    path('providers/<int:pk>/', provider_detail, name='provider-detail'),
]
