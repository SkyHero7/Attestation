from django.contrib import admin
from .models import NetworkElement, Product


@admin.register(NetworkElement)
class NetworkElementAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'supplier', 'debt', 'created_at')
    list_filter = ('city',)
    search_fields = ('name',)

    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        queryset.update(debt=0)
    clear_debt.short_description = 'Clear debt for selected elements'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date', 'network_element')
