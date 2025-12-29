from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'state', 'pincode', 'user_type']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )


    class Meta:

        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update User fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile = instance.profile
            profile.phone = profile_data.get('phone', profile.phone)
            profile.address = profile_data.get('address', profile.address)
            profile.city = profile_data.get('city', profile.city)
            profile.state = profile_data.get('state', profile.state)
            profile.pincode = profile_data.get('pincode', profile.pincode)
            profile.user_type = profile_data.get('user_type', profile.user_type)
            profile.save()
            
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:

        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user_type = profile_data.get('user_type', 'customer')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=(user_type == 'admin')
        )
        UserProfile.objects.create(user=user, **profile_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


