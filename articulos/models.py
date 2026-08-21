from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    sku = models.CharField(
        max_length=50, unique=True, verbose_name="Código SKU"
    )
    nombre = models.CharField(
        max_length=200, verbose_name="Nombre del Producto"
    )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, verbose_name="Categoría"
    )
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio de Venta"
    )
    stock_actual = models.IntegerField(
        default=0, verbose_name="Existencias en Almacén"
    )
    stock_minimo = models.IntegerField(
        default=5, verbose_name="Stock Mínimo Permitido"
    )

    def __str__(self):
        return f"{self.sku} - {self.nombre}"
