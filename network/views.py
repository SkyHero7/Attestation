from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import BasePermission
from .forms import NetworkElementForm

from .models import NetworkElement, Product
from .serializers import NetworkElementSerializer, ProductSerializer

def home(request):
    elements = NetworkElement.objects.all()
    context = {
        'elements': elements,
    }
    return render(request, 'network/home.html', context)

def all_elements(request):
    elements = NetworkElement.objects.all()
    return render(request, 'network/all_elements.html', {'elements': elements})


def add_element(request):
    if request.method == 'POST':
        form = NetworkElementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_elements')
    else:
        form = NetworkElementForm()

    return render(request, 'network/add_element.html', {'form': form})

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