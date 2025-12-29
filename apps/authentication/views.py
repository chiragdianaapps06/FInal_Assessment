from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.activity_logs.utils import create_activity_log


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            
            # Log login activity
            create_activity_log(
                user=user,
                action="User Login",
                entity_type="User",
                entity_id=user.id,
                details={"username": user.username},
                request=request
            )
            
            return Response({
                'message': 'Login successful',
                'token':{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
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
        return self.request.user

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({
                'message': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request):
        return Response({
            "message": "Hello Admin!"
        }, status=status.HTTP_200_OK)


