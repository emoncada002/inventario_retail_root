from articulos.models import Producto
from django.db import models


class InventarioDAO:
    """
    Data Access Object (DAO) para centralizar la persistencia y
    operaciones CRUD del inventario de Retail.
    """

    @staticmethod
    def obtener_todo_el_inventario():
        # Consulta el catálogo completo de productos con su categoría
        return Producto.objects.all().select_related('categoria')

    @staticmethod
    def consultar_alertas_stock_critico():
        # Filtra productos cuyas existencias están en niveles mínimos de riesgo
        return Producto.objects.filter(
            stock_actual__lte=models.F('stock_minimo')
        )

    @staticmethod
    def insertar_nuevo_producto(
        sku, nombre, categoria_id, precio, stock_inicial, stock_min
    ):
        # Inserta de forma segura un nuevo artículo en el catálogo de retail
        nuevo_producto = Producto(
            sku=sku,
            nombre=nombre,
            categoria_id=categoria_id,
            precio=precio,
            stock_actual=stock_inicial,
            stock_minimo=stock_min
        )
        nuevo_producto.save()
        return nuevo_producto
