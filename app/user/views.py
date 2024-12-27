from django.template.context_processors import request
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenVerifyView,
                                            TokenRefreshView)

from app.common.utils import update_model
from app.user.models import User, Address
from app.user.permissions import IsOwnerOrAdminUser
from app.user.serializers import (ProfileSerializer,
                                  AddressSerializer,
                                  CustomTokenObtainPairSerializer)

profile_tags = ['Profiles']
address_tags = ['Addresses']
token_tags = ['Token']


class ProfileAPIView(APIView):
    """
    Views user`s profile
    """

    serializer_class = ProfileSerializer

    @extend_schema(
        summary='Get profile',
        description='View to get profile',
        tags=profile_tags
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Registration',
        description='View to create a new user',
        tags=token_tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer. is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            serializer = self.serializer_class(user)
            data = serializer.data

            refresh = RefreshToken.for_user(user)
            data.setdefault('refresh', str(refresh))
            data.setdefault('access', str(refresh.access_token))
            data.setdefault('is_admin', request.user.is_admin)
            data.pop('address')

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Update profile',
        description='View to update profile',
        tags=profile_tags
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = update_model(user, serializer.validated_data)
            user.save()
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete user',
        description='View to delete user',
        tags=profile_tags
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['GET', 'UPDATE', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class AddressAPIView(APIView):
    """
    Views to get or create user`s addresses
    """

    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get addresses',
        description='View to get addresses',
        tags=address_tags
    )
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)

        if not addresses:
            return Response({'message': 'Addresses not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Create a new address',
        description='View to create a new address',
        tags=address_tags
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            if Address.objects.filter(user=request.user,
                                      **serializer.validated_data).exists():
                return Response({'message': 'You already have this address'})

            address = Address.objects.create(user=request.user,
                                             **serializer.validated_data)
            serializer = self.serializer_class(address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressByIdAPIView(APIView):
    """
    Views to update or delete address by pk
    """
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrAdminUser]

    def get_object(self, pk):
        try:
            address = Address.objects.get(pk=pk)
            self.check_object_permissions(self.request, address)
            return address
        except Address.DoesNotExist:
            return None

    @extend_schema(
        summary='Get address',
        description='View to get address by pk',
        tags=address_tags
    )
    def get(self, request, *args, **kwargs):
        address = self.get_object(kwargs.get('pk'))

        if not address:
            return Response({'message': 'Addresses not found'},
                            status=status.HTTP_404_NOT_FOUND)

        # if address.user != request.user and not request.user.is_admin:
        #     return Response({'message': 'You not the owner of this address'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Update address',
        description='View to update address by pk',
        tags=address_tags
    )
    def put(self, request, *args, **kwargs):
        address = self.get_object(kwargs.get('pk'))

        if not address:
            return Response({'message': 'Addresses not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            address = update_model(address, serializer.validated_data)
            address.save()
            serializer = self.serializer_class(address)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete address',
        description='View to delete address by pk',
        tags=address_tags
    )
    def delete(self, request, *args, **kwargs):
        address = self.get_object(kwargs.get('pk'))

        if not address:
            return Response({'message': 'Addresses not found'},
                            status=status.HTTP_404_NOT_FOUND)

        address.is_active = False
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView for description methods
    """
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary='Authorization',
        description='View to authorization',
        tags=token_tags
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom TokenRefreshView for description methods
    """

    @extend_schema(
        summary='Refresh token',
        description='View to refresh token',
        tags=token_tags
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom TokenVerifyView for description methods
    """

    @extend_schema(
        summary='Verify token',
        description='View to verify token',
        tags=token_tags
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
