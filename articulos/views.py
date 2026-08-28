from django.shortcuts import render, redirect
from articulos.dao.inventariodao import InventarioDAO
from articulos.models import Producto, Categoria


def dashboard_retail(request):
    """
    Controlador definitivo de la Fase 3.
    Aprovecha la arquitectura nativa de Django separando la lógica del HTML/CSS
    y consolidando el ciclo CRUD completo (Altas, Bajas, Cambios, Consultas).
    """
    pestaana = request.GET.get('pestaana', 'tablero')
    usuario_activo = request.GET.get('usuario', 'E. Moncada')
    siguiente_usuario = (
        "Sergio Salcedo" if usuario_activo == "E. Moncada" else "E. Moncada"
    )

    # Garantizar la existencia de categorías base en db.sqlite3
    if not Categoria.objects.exists():
        Categoria.objects.create(
            nombre="Ropa", descripcion="Prendas de vestir"
        )
        Categoria.objects.create(
            nombre="Calzado", descripcion="Zapatos y tenis"
        )
        Categoria.objects.create(
            nombre="Accesorios", descripcion="Gorras y mochilas"
        )

    # PROCESAMIENTO DE PETICIONES POST (ACCIONES CRUD)
    if request.method == "POST":
        accion = request.POST.get('accion')

        if accion == "guardar_producto":
            cat = Categoria.objects.get(nombre=request.POST.get('categoria'))
            InventarioDAO.insertar_nuevo_producto(
                sku=request.POST.get('sku'),
                nombre=request.POST.get('nombre'),
                categoria_id=cat.id,
                precio=request.POST.get('precio'),
                stock_inicial=request.POST.get('stock'),
                stock_min=5
            )
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "actualizar_producto":
            # OPERACIÓN DE ACTUALIZACIÓN
            sku = request.POST.get('sku')
            prod = Producto.objects.get(sku=sku)
            cat = Categoria.objects.get(nombre=request.POST.get('categoria'))

            prod.nombre = request.POST.get('nombre')
            prod.categoria = cat
            prod.precio = request.POST.get('precio')
            prod.stock_actual = int(request.POST.get('stock'))
            prod.save()  # Guarda los cambios modificados de manera permanente
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "procesar_movimiento":
            prod = Producto.objects.get(sku=request.POST.get('sku_afectado'))
            cantidad = int(request.POST.get('cantidad', 0))
            if "Entrada" in request.POST.get('tipo_flujo'):
                prod.stock_actual += cantidad
            else:
                prod.stock_actual = max(0, prod.stock_actual - cantidad)
            prod.save()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

        elif accion == "eliminar_producto":
            prod = Producto.objects.get(sku=request.POST.get('sku_a_borrar'))
            prod.delete()
            return redirect(f"/?pestaana=tablero&usuario={usuario_activo}")

    # EXTRACCIÓN DE DATOS REALES UTILIZANDO EL PATRÓN DAO
    productos_db = InventarioDAO.obtener_todo_el_inventario()
    alertas_db = InventarioDAO.consultar_alertas_stock_critico()

    # Preparamos el contexto inicial para los archivos HTML
    contexto = {
        'pestaana': pestaana,
        'usuario_activo': usuario_activo,
        'siguiente_usuario': siguiente_usuario,
        'productos': productos_db,
        'alertas': alertas_db,
    }

    # LÓGICA DE RENDERIZACIÓN SEGÚN LA PESTAÑA SELECCIONADA
    if pestaana == 'registro':
        return render(request, 'mainvista/almacen.html', contexto)
    elif pestaana == 'editar':
        sku_editar = request.GET.get('sku_editar')
        contexto['prod_a_editar'] = Producto.objects.get(sku=sku_editar)
        return render(request, 'mainvista/almacen.html', contexto)
    elif pestaana == 'movimientos':
        return render(request, 'mainvista/movimientos.html', contexto)

    # Por defecto carga el Tablero General
    return render(request, 'mainvista/tablero.html', contexto)
