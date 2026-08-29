import os
import io
import csv
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.contrib import admin
from articulos.models import Producto, Categoria
from django import forms


# Formulario para importar archivos csv
class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label="Selecciona un archivo CSV")

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

    change_list_template = "admin/productos_list.html"

    actions = ['cargar_csv_action']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('importar-csv/', self.admin_site.admin_view(self.importar_csv), name='producto_importar_csv'),
        ]
        return custom_urls + urls

    def importar_csv(self, request):
        """Vista integrada que genera la pantalla de subida con el diseño predeterminado de Django Admin"""
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'El archivo debe tener extensión .csv')
                    return redirect('.')

                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string, None)  # Omitir la primera línea (encabezados)

                contador = 0
                for row in csv.reader(io_string, delimiter=','):
                    if row:
                        Producto.objects.create(
                            nombre=row[0].strip(),
                            precio=row[1].strip(),
                            categoria=row[2].strip().upper()
                        )
                        contador += 1

                messages.success(request, f'¡Se cargaron {contador} productos correctamente!')
                return redirect('..')
        else:
            form = CsvImportForm()

        context = {
            'form': form,
            'title': 'Cargue Masivo de Productos (CSV)',
            'site_header': admin.site.site_header,
            'opts': self.model._meta,
        }
        return render(request, "admin/change_form.html", context)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
