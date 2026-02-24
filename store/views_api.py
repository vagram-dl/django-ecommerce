from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics,viewsets
from rest_framework.decorators import permission_classes

from .models import Product,Category
from .serializers import ProductSerializer,CategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permission_classes= [AllowAny]
        elif self.action in ['create','update','partial_update','destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category__slug']

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['create']:
            permission_classes = [IsAdminUser]
        elif self.action in ['update','partial_update']:
            permission_classes = [IsAdminUser]
        elif self.action in ['destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]