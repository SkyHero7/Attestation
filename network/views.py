from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import BasePermission

from .models import NetworkElement, Product
from .serializers import NetworkElementSerializer, ProductSerializer
from .forms import NetworkElementForm, ProductForm


def home(request):
    elements = NetworkElement.objects.all()
    context = {
        'elements': elements,
    }
    return render(request, 'network/home.html', context)

def all_elements(request):
    city_filter = request.GET.get('city', '')
    if city_filter:
        elements = NetworkElement.objects.filter(city__icontains=city_filter)
    else:
        elements = NetworkElement.objects.all()
    return render(request, 'network/all_elements.html', {'elements': elements, 'city_filter': city_filter})


def add_element(request):
    if request.method == 'POST':
        form = NetworkElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)

            # Если поле supplier не указано, устанавливаем уровень и скрываем debt и supplier
            if not element.supplier:
                element.level = 0
                element.debt = None
                element.supplier = None
            else:
                previous_element = NetworkElement.objects.get(pk=element.supplier.id)
                element.level = previous_element.level + 1

            element.save()
            return redirect('home')
    else:
        form = NetworkElementForm()

    return render(request, 'network/add_element.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление на главную страницу после успешного добавления
    else:
        form = ProductForm()
    return render(request, 'network/add_product.html', {'form': form})

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

def element_detail(request, pk):
    element = get_object_or_404(NetworkElement, pk=pk)
    return render(request, 'network/element_detail.html', {'element': element})

def clear_debt(request, pk):
    element = get_object_or_404(NetworkElement, pk=pk)
    if request.method == 'POST':
        if element.debt != 0:
            element.debt = 0
            element.save()
        return redirect('element_detail', pk=pk)