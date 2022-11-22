from rest_framework import serializers

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password

from .models import User
# User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = (
            "id", 
            "username", 
            "email", 
            "password", 
            "full_name",
            "is_active",
            "is_staff"
        )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserCreateSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id", 
            "username", 
            "email", 
            "full_name",
            "is_active",
            "is_staff"
        )


class UserReadSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = (
            "id", 
            "username",
            "full_name"
        )
