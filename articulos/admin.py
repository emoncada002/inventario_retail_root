from django.contrib import admin
from articulos.models import Producto, Categoria


# Configuración avanzada para ver el SKU y las existencias en forma de
# tabla en el admin
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'nombre',
        'categoria',
        'precio',
        'stock_actual',
        'stock_minimo',
    )
    list_filter = ('categoria',)
    search_fields = ('sku', 'nombre')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
