from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Service, ServiceProvider
from .serializers import ServiceSerializer, ServiceProviderSerializer
from .paginations import StandardResultsSetPagination
from apps.activity_logs.utils import create_activity_log
from rest_framework import status
from django.db.models import Q
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_create(self, serializer):
        service = serializer.save()
        create_activity_log(
            user=self.request.user,
            action="Service Created",
            entity_type="Service",
            entity_id=service.id,
            details={"name": service.name, "base_price": str(service.base_price)},
            request=self.request
        )

    def perform_update(self, serializer):
        service = serializer.save()
        create_activity_log(
            user=self.request.user,
            action="Service Updated",
            entity_type="Service",
            entity_id=service.id,
            details={"name": service.name, "is_active": service.is_active},
            request=self.request
        )

    def perform_destroy(self, instance):
        create_activity_log(
            user=self.request.user,
            action="Service Deleted",
            entity_type="Service",
            entity_id=instance.id,
            details={"name": instance.name},
            request=self.request
        )
        instance.delete()


    @action(detail=False, methods=['get'], url_path='search')
    def search_services(self, request):
        query = request.query_params.get('q', '')

        if not query:
            return Response(
                {"message": "No search query provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Search results retrieved successfully",
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )



class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
