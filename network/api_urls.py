from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkElementViewSet, ProductViewSet

# Создание маршрутизатора для автоматического управления URL-адресами
router = DefaultRouter()

# Регистрация ViewSet для сетевых элементов
router.register(r'network-elements', NetworkElementViewSet)
# Регистрация ViewSet для продуктов
router.register(r'products', ProductViewSet)

urlpatterns = [
    # Включение URL-адресов, управляемых маршрутизатором
    path('', include(router.urls)),
]
