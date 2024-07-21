from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Supplier


class SupplierTests(APITestCase):
    """
    Тесты для модели Supplier.

    Проверяет создание, получение и фильтрацию поставщиков.
    """

    def setUp(self):
        """
        Настройка начальных данных для тестов.

        Создает пользователя, выполняет вход и получает JWT токен для авторизации.
        """
        # Создаем пользователя и получаем токен
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Получаем JWT токен
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_supplier(self):
        """
        Тест создания нового поставщика.

        Отправляет POST запрос на создание нового поставщика и проверяет,
        что поставщик был успешно создан и сохранен в базе данных.
        """
        url = reverse('supplier-list')
        data = {
            'name': 'Test Supplier',
            'email': 'supplier@example.com',
            'country': 'Test Country',
            'city': 'Test City',
            'street': 'Test Street',
            'house_number': '123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(Supplier.objects.get().name, 'Test Supplier')

    def test_list_suppliers(self):
        """
        Тест получения списка поставщиков.

        Создает два поставщика и отправляет GET запрос на получение списка всех поставщиков.
        Проверяет, что в ответе содержится два поставщика.
        """
        Supplier.objects.create(name='Supplier 1', email='supplier1@example.com', country='Country 1', city='City 1',
                                street='Street 1', house_number='1')
        Supplier.objects.create(name='Supplier 2', email='supplier2@example.com', country='Country 2', city='City 2',
                                street='Street 2', house_number='2')
        url = reverse('supplier-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_suppliers_by_country(self):
        """
        Тест фильтрации поставщиков по стране.

        Создает два поставщика с разными странами и отправляет GET запрос с параметром
        фильтрации по стране. Проверяет, что в ответе содержится только поставщик с указанной страной.
        """
        Supplier.objects.create(name='Supplier 1', email='supplier1@example.com', country='Country 1', city='City 1',
                                street='Street 1', house_number='1')
        Supplier.objects.create(name='Supplier 2', email='supplier2@example.com', country='Country 2', city='City 2',
                                street='Street 2', house_number='2')
        url = reverse('supplier-list') + '?search=Country 1'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country'], 'Country 1')
