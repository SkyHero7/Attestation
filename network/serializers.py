# serializers.py
from rest_framework import serializers
from .models import NetworkElement, Product, Supplier

class NetworkElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkElement
        fields = '__all__'
        read_only_fields = ['debt']  # Запретить обновление поля 'debt'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'country', 'city', 'street', 'house_number', 'debt']

    def update(self, instance, validated_data):
        validated_data.pop('debt', None)  # Запретить обновление поля 'debt'
        return super().update(instance, validated_data)
