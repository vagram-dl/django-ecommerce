from django.urls import path
from .views_api import ProductListView,ProductDetailView

urlpatterns = [
    path('api/products/',ProductListView.as_view(),name = 'api_products'),
    path('api/products/<int:pk>',ProductDetailView.as_view(),name='api_product_detail'),
]