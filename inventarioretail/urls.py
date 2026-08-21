from django.contrib import admin
from django.urls import path
from articulos import views

urlpatterns = [
    path(
        'admin/',
        admin.site.split if hasattr(admin.site, 'split') else admin.site.urls,
    ),
    # Pantalla principal del inventario
    path('', views.dashboard_retail, name='dashboard'),
]
