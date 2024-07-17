from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import BasePermission

from .models import NetworkElement, Product
from .serializers import NetworkElementSerializer, ProductSerializer

class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)

class NetworkElementViewSet(viewsets.ModelViewSet):
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer
    permission_classes = [IsActiveUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveUser]