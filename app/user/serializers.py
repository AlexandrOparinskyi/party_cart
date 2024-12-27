from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.user.models import User


class AddressSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    street = serializers.CharField(max_length=100)
    house = serializers.CharField(max_length=20)
    apartment = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=255, allow_null=True)
    full_address = serializers.CharField(read_only=True,
                                         source='get_full_address')


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = AddressSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with this email already exists.')
        return email

    def validate_phone(self, phone):
        if User.objects.filter(phone=phone).exists():
            raise ValidationError('User with this phone already exists.')
        return phone


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to added fields
    """

    def validate(self, attrs):
        token = super().validate(attrs)
        token['is_admin'] = self.user.is_admin
        return token
