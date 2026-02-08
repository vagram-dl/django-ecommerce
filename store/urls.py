from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import ProductViewSet,CategoryViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'products',ProductViewSet,basename = 'product')
router.register(r'categories',CategoryViewSet,basename = 'category')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/',TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name = 'token_refresh'),
]