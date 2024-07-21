from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404

from .models import NetworkElement, Product, Supplier
from .serializers import NetworkElementSerializer, ProductSerializer, SupplierSerializer
from .forms import NetworkElementForm, ProductForm


def home(request):
    """
    Представление домашней страницы.

    Запрашивает все элементы сети и передает их в контексте шаблона.
    """
    elements = NetworkElement.objects.all()
    context = {
        'elements': elements,
    }
    return render(request, 'network/home.html', context)


def all_elements(request):
    """
    Представление для отображения всех элементов сети с фильтрацией по городу.

    Фильтрует элементы по полю 'city', если задан параметр 'city' в запросе.
    """
    city_filter = request.GET.get('city', '')
    if city_filter:
        elements = NetworkElement.objects.filter(city__icontains=city_filter)
    else:
        elements = NetworkElement.objects.all()
    return render(request, 'network/all_elements.html', {'elements': elements, 'city_filter': city_filter})


def add_element(request):
    """
    Представление для добавления нового элемента сети.

    Обрабатывает форму добавления элемента и сохраняет новый элемент в базе данных.
    """
    if request.method == 'POST':
        form = NetworkElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
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
    """
    Представление для добавления нового продукта.

    Обрабатывает форму добавления продукта и сохраняет новый продукт в базе данных.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'network/add_product.html', {'form': form})


def element_detail(request, pk):
    """
    Представление для отображения деталей конкретного элемента сети.

    Запрашивает элемент по его идентификатору, а также связанные с ним элементы и их задолженность.
    """
    element = get_object_or_404(NetworkElement, pk=pk)
    supplied_elements = NetworkElement.objects.filter(supplier=element)
    total_debt = sum(e.debt for e in supplied_elements if e.debt < 0)
    total_balance = sum(e.debt for e in supplied_elements if e.debt >= 0)
    context = {
        'element': element,
        'supplied_elements': supplied_elements,
        'total_debt': abs(total_debt),
        'total_balance': total_balance,
    }
    return render(request, 'network/element_detail.html', context)


def clear_debt(request, pk):
    """
    Представление для очистки задолженности у конкретного элемента.

    Устанавливает задолженность элемента в 0 при POST-запросе и перенаправляет на страницу деталей элемента.
    """
    element = get_object_or_404(NetworkElement, pk=pk)
    if request.method == 'POST':
        if element.debt != 0:
            element.debt = 0
            element.save()
        return redirect('element_detail', pk=pk)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления поставщиками.

    Предоставляет стандартные операции CRUD для модели Supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']


class NetworkElementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления элементами сети.

    Предоставляет стандартные операции CRUD для модели NetworkElement.
    """
    queryset = NetworkElement.objects.all()
    serializer_class = NetworkElementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления продуктами.

    Предоставляет стандартные операции CRUD для модели Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
