from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('all-elements/', views.all_elements, name='all_elements'),
    path('add-element/', views.add_element, name='add_element'),
]
