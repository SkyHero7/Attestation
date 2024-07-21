# serializers.py
from rest_framework import serializers
from .models import NetworkElement, Product, Supplier


class NetworkElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NetworkElement.

    Позволяет преобразовывать данные модели NetworkElement в JSON и обратно.

    Поля:
        - id: Идентификатор элемента сети.
        - name: Название элемента сети.
        - email: Электронная почта.
        - country: Страна.
        - city: Город.
        - street: Улица.
        - house_number: Номер дома.
        - created_at: Дата и время создания.
        - supplier: Поставщик (если есть).
        - debt: Долг (только для чтения).
        - level: Уровень элемента сети.
    """
    class Meta:
        model = NetworkElement
        fields = '__all__'
        read_only_fields = ['debt']  # Запретить обновление поля 'debt'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Позволяет преобразовывать данные модели Product в JSON и обратно.

    Поля:
        - id: Идентификатор продукта.
        - name: Название продукта.
        - model: Модель продукта.
        - release_date: Дата выпуска.
        - network_element: Элемент сети, к которому относится продукт.
    """
    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Supplier.

    Позволяет преобразовывать данные модели Supplier в JSON и обратно.

    Поля:
        - id: Идентификатор поставщика.
        - name: Название поставщика.
        - email: Электронная почта.
        - country: Страна.
        - city: Город.
        - street: Улица.
        - house_number: Номер дома.
        - debt: Долг.
    """
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'country', 'city', 'street', 'house_number', 'debt']

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр модели Supplier.

        Аргументы:
            instance (Supplier): Экземпляр модели, который нужно обновить.
            validated_data (dict): Данные, прошедшие проверку.

        Возвращает:
            Supplier: Обновленный экземпляр модели.
        """
        validated_data.pop('debt', None)  # Запретить обновление поля 'debt'
        return super().update(instance, validated_data)
