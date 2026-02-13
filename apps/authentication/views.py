from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.activity_logs.utils import create_activity_log
import logging

logger = logging.getLogger('debug')


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            
            logger.info("User '%s' logged in successfully from IP %s", user.username, request.META.get('REMOTE_ADDR'))

            # Log login activity
            create_activity_log(
                user=user,
                action="User Login",
                entity_type="User",
                entity_id=user.id,
                details={"username": user.username},
                request=request
            )
            logger.info(f"user logged in successfully {user},{user.id}")
            return Response({
                'message': 'Login successful',
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        logger.warning("Failed login attempt for data: %s", {k: v for k, v in request.data.items() if k != 'password'})
        return Response({
            'message': 'Invalid credentials',
            **serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        
        logger.info("New user registered: '%s' (email: %s)", user.username, user.email)

        # Log registration activity
        create_activity_log(
            user=user,
            action="User Registration",
            entity_type="User",
            entity_id=user.id,
            details={"username": user.username, "email": user.email},
            request=self.request
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        logger.info("User '%s' fetched profile from IP %s", self.request.user.username, self.request.META.get('REMOTE_ADDR'))
        return self.request.user

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User '%s' logged out successfully", request.user.username)
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error("Logout failed for user '%s': %s", request.user.username, str(e))
            return Response({
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        return Response({
            "message": "Hello Admin!"
        }, status=status.HTTP_200_OK)