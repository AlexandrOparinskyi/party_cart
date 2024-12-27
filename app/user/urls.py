from django.urls import path

from app.user.views import (ProfileAPIView,
                            AddressAPIView,
                            CustomTokenObtainPairView,
                            CustomTokenVerifyView,
                            CustomTokenRefreshView, AddressByIdAPIView)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/verify/', CustomTokenVerifyView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('address/', AddressAPIView.as_view()),
    path('address/<uuid:pk>', AddressByIdAPIView.as_view())
]
