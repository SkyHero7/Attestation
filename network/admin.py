from django.contrib import admin
from .models import NetworkElement, Product


@admin.register(NetworkElement)
class NetworkElementAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления объектами NetworkElement.

    Отображает список сетевых элементов с именем, городом, поставщиком, долгом и датой создания.
    Предоставляет фильтрацию по городу и поиск по имени.
    Включает действие для очистки долга у выбранных сетевых элементов.
    """
    list_display = ('name', 'city', 'supplier', 'debt', 'created_at')
    list_filter = ('city',)
    search_fields = ('name',)

    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        """
        Действие для очистки долга у выбранных сетевых элементов.

        Аргументы:
            request: Объект запроса.
            queryset: Выбранные объекты сетевых элементов.

        """
        queryset.update(debt=0)
    clear_debt.short_description = 'Очистить долг для выбранных элементов'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для управления объектами Product.

    Отображает список продуктов с именем, моделью, датой выпуска и связанной сетевой элементом.
    """
    list_display = ('name', 'model', 'release_date', 'network_element')
