from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    pass


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
