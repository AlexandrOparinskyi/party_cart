from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.common.utils import update_model
from app.user.models import User
from app.user.serializers import ProfileSerializer

tags = ['Profiles']


class ProfileAPIView(APIView):
    """
    View user`s profile
    """

    serializer_class = ProfileSerializer

    @extend_schema(
        summary='Get profile',
        description='View to get profile',
        tags=tags
    )
    def get(self, request):
        user = User.objects.get(pk=request.user.pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Update profile',
        description='View to update profile',
        tags=tags
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
        tags=tags
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
