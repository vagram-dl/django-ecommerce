from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics,viewsets
from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug']
