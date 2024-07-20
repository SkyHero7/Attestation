from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import NetworkElement, Product, Supplier
from .serializers import NetworkElementSerializer, ProductSerializer, SupplierSerializer
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
    # Получаем все объекты, у которых текущий элемент является поставщиком
    supplied_elements = NetworkElement.objects.filter(supplier=element)

    # Рассчитываем суммы задолженностей и остатков
    total_debt = sum(e.debt for e in supplied_elements if e.debt < 0)
    total_balance = sum(e.debt for e in supplied_elements if e.debt >= 0)

    context = {
        'element': element,
        'supplied_elements': supplied_elements,
        'total_debt': abs(total_debt),  # Убираем знак минуса для общего долга
        'total_balance': total_balance,
    }
    return render(request, 'network/element_detail.html', context)

def clear_debt(request, pk):
    element = get_object_or_404(NetworkElement, pk=pk)
    if request.method == 'POST':
        if element.debt != 0:
            element.debt = 0
            element.save()
        return redirect('element_detail', pk=pk)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']