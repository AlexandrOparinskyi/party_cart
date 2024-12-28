from django.urls import path

from app.product.views import (CategoryAPIView,
                               CategoryBySlugAPIView,
                               ProductsAPIView,
                               ProductBySlugAPIView,
                               ProductByCategoryAPIView)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view()),
    path('category/<slug:slug>/', CategoryBySlugAPIView.as_view()),
    path('products/', ProductsAPIView.as_view()),
    path('product/<slug:slug>/', ProductBySlugAPIView.as_view()),
    path('products/<slug:category_slug>/', ProductByCategoryAPIView.as_view())
]