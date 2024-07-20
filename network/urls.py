from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('all-elements/', views.all_elements, name='all_elements'),
    path('add-element/', views.add_element, name='add_element'),
    path('add-product/', views.add_product, name='add_product'),
    path('element/<int:pk>/', views.element_detail, name='element_detail'),
    path('element/<int:pk>/clear-debt/', views.clear_debt, name='clear_debt'),
]
