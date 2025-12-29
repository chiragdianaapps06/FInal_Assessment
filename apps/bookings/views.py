from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer, BookingStatusUpdateSerializer
from apps.activity_logs.utils import create_activity_log


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['booking_number', 'customer__username', 'service__name']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Booking.objects.all()
        else:
            queryset = Booking.objects.filter(customer=user)
        
        # Filtering
        status_param = self.request.query_params.get('status')
        date_param = self.request.query_params.get('date')
        
        if status_param:
            queryset = queryset.filter(status=status_param)
        if date_param:
            queryset = queryset.filter(scheduled_date__date=date_param)
            
        return queryset.order_by('-created_at')


    def perform_create(self, serializer):
        booking = serializer.save(customer=self.request.user)
        
        # Log booking creation
        create_activity_log(
            user=self.request.user,
            action="Booking Created",
            entity_type="Booking",
            entity_id=booking.id,
            details={"booking_number": booking.booking_number, "service": booking.service.name},
            request=self.request
        )


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            return Response({
                "message": "Cannot cancel booking after it has been confirmed or started."
            }, status=status.HTTP_400_BAD_REQUEST)
        instance.status = 'cancelled'
        instance.save()
        
        # Log booking cancellation
        create_activity_log(
            user=request.user,
            action="Booking Cancelled",
            entity_type="Booking",
            entity_id=instance.id,
            details={"booking_number": instance.booking_number},
            request=request
        )
        
        return Response({
            'message': 'Booking cancelled successfully'
        }, status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['patch'], url_path='status', permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        booking = self.get_object()
        old_status = booking.status
        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            # Log status update
            create_activity_log(
                user=request.user,
                action="Booking Status Updated",
                entity_type="Booking",
                entity_id=booking.id,
                details={
                    "booking_number": booking.booking_number,
                    "old_status": old_status,
                    "new_status": booking.status
                },
                request=request
            )
            
            return Response({
                'message': 'Booking status updated successfully',
                **serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Validation error',
            **serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['get'], url_path='admin/all', permission_classes=[permissions.IsAdminUser])
    def admin_all_bookings(self, request):
        bookings = Booking.objects.all()
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
