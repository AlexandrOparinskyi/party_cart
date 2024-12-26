from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from app.user.views import ProfileAPIView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', ProfileAPIView.as_view())
]