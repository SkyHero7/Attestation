from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import home, NetworkElementViewSet, SupplierViewSet
from . import views

router = DefaultRouter()
router.register(r'network-elements', NetworkElementViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('all-elements/', views.all_elements, name='all_elements'),
    path('add-element/', views.add_element, name='add_element'),
    path('add-product/', views.add_product, name='add_product'),
    path('element/<int:pk>/', views.element_detail, name='element_detail'),
    path('element/<int:pk>/clear-debt/', views.clear_debt, name='clear_debt'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls)),
]