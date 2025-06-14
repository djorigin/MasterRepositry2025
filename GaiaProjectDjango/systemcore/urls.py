"""
URL configuration for System Core App.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import (HomeView, ColorCodeListView,
                    ColorCodeCreateView, ColorCodeDetailView,
                    RJ45PinoutBulkCreateView, RJ45PinoutListView,
                    RJ45PinoutDetailView, RJ45PinoutUpdateView,
                    RJ45PinoutDeleteView, RJ45PinDeleteView, RJ45PinUpdateView,
                    SupplierCreateView, SupplierListView, SupplierDetailView,
                    SupplierUpdateView, SupplierDeleteView)

app_name = 'systemcore'

# URL patterns for the systemcore app   

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('colorcode_create/', views.ColorCodeCreateView.as_view(), name='colorcode_create'),
    path('colorcodes/', ColorCodeListView.as_view(), name='colorcode_list'),
    path('colorcodes/<int:pk>/', ColorCodeDetailView.as_view(), name='colorcode_detail'),
    
    path('rj45pinout/bulk-create/', RJ45PinoutBulkCreateView.as_view(), name='rj45pinout_bulk_create'),
    path('rj45pinout/', RJ45PinoutListView.as_view(), name='rj45pinout_list'),
    path('rj45pinout/<int:pk>/', RJ45PinoutDetailView.as_view(), name='rj45pinout_detail'),
    path('rj45pinout/<int:pk>/edit/', RJ45PinoutUpdateView.as_view(), name='rj45pinout_edit'),
    path('rj45pinout/<int:pk>/delete/', RJ45PinoutDeleteView.as_view(), name='rj45pinout_delete'),
    path('rj45pin/<int:pk>/edit/', RJ45PinUpdateView.as_view(), name='rj45pin_edit'),
    path('rj45pin/<int:pk>/delete/', RJ45PinDeleteView.as_view(), name='rj45pin_delete'),
    
    path('suppliers/new/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/<str:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),
    path('suppliers/<str:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_edit'),
    path('suppliers/<str:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
    
]


